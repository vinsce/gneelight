import threading

from yeelight import discover_bulbs, Bulb

from constants import *

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


# TODO add predefined options
# TODO add bulb info section
# TODO add delay off option
# TODO add color selection


# noinspection PyArgumentList
class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=APP_NAME)
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(400, 400)

        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = APP_NAME
        self.set_titlebar(self.header_bar)
        self.refresh_button = Gtk.Button()
        icon = Gio.ThemedIcon(name="view-refresh-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.refresh_button.add(image)
        self.header_bar.pack_end(self.refresh_button)
        self.refresh_button.connect('clicked', self.start_discovery)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.set_vexpand(True)
        self.add(self.box)

        self.spinner = Gtk.Spinner()

        self.bulbs_combo = Gtk.ComboBoxText()
        self.bulbs_combo.set_entry_text_column(0)
        self.bulbs_combo.connect("changed", self.on_bulb_selected)
        self.bulbs_combo.set_hexpand(False)
        self.bulbs_combo.set_halign(Gtk.Align.CENTER)
        self.bulbs_combo.set_size_request(200, -1)

        self.discovered_bulbs = None
        self.bulb_ip = None
        self.bulb = None

        self.init_control_layout()
        self.no_result_box = None

        self.start_discovery()

    # noinspection PyAttributeOutsideInit
    def init_control_layout(self):
        self.control_box = Gtk.ListBox()
        self.control_box.set_selection_mode(Gtk.SelectionMode.NONE)
        row = BulbOptionRow()

        self.power_switch = Gtk.Switch()
        self.power_switch.props.valign = Gtk.Align.CENTER
        self.power_switch.connect('state-set', self.toggle_bulb)

        row.set_content(Gtk.Label(label="Power", xalign=0), self.power_switch, control_expand=False)

        self.control_box.add(row)

        row2 = BulbOptionRow()
        self.brightness_slider = Gtk.Scale.new_with_range(orientation=Gtk.Orientation.HORIZONTAL, min=1, max=100, step=1)
        self.brightness_slider.connect("button-release-event", self.change_brightness)

        row2.set_content(Gtk.Label(label="Brightness", xalign=0), self.brightness_slider)
        self.control_box.add(row2)

    # noinspection PyUnusedLocal
    def toggle_bulb(self, widget, status):
        MainWindow.run_in_thread(target=self.toggle_sync, status=status)

    def toggle_sync(self, status):
        if status:
            self.bulb.turn_on()
        else:
            self.bulb.turn_off()
        self.update_status_sync()

    def show_loading(self, loading, control_only=False):
        if loading:
            if not control_only:
                self.box.remove(self.bulbs_combo)
            self.box.remove(self.control_box)
            if self.no_result_box:
                self.box.remove(self.no_result_box)
            self.spinner.start()
            self.box.pack_start(self.spinner, True, True, 150)
        else:
            self.spinner.stop()
            self.box.remove(self.spinner)
        self.box.show_all()

    def discovery(self):
        self.discovered_bulbs = discover_bulbs()

        self.show_loading(False)

        if len(self.discovered_bulbs) > 0:
            self.bulbs_combo.remove_all()

            for bulb in self.discovered_bulbs:
                self.bulbs_combo.append_text(bulb.get('ip') + ":" + str(bulb.get('port')))

            self.box.pack_start(self.bulbs_combo, False, False, 6)
            self.bulbs_combo.set_active(0)
        else:
            self.show_no_result()
        self.box.show_all()

    def on_bulb_selected(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.bulb_ip = model[tree_iter][0].split(':')[0]
            print("Selected: bulb=%s" % self.bulb_ip)
            self.start_bulb_connection()
        else:
            pass

    # noinspection PyUnusedLocal
    def change_brightness(self, widget, event):
        bright = self.brightness_slider.get_value()
        MainWindow.run_in_thread(self.change_brightness_sync, brightness=bright)

    def change_brightness_sync(self, brightness):
        self.bulb.set_brightness(brightness=brightness)
        self.update_status()

    def update_status(self):
        MainWindow.run_in_thread(target=self.update_status_sync)

    def update_status_sync(self):
        bulb_properties = self.bulb.get_properties()
        print(bulb_properties)

        self.power_switch.set_active(bulb_properties.get('power') == 'on')
        self.brightness_slider.set_value(int(bulb_properties.get('bright')))
        self.control_box.show_all()

    def show_no_result(self):
        self.no_result_box = Gtk.VBox(homogeneous=False)

        pixbuf = Gtk.IconTheme.get_default().load_icon('computer-fail-symbolic', 64, 0)

        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        label = Gtk.Label(label='No bulb found')
        button = Gtk.Button(label='Retry')
        button.connect("clicked", self.start_discovery)
        button.set_hexpand(False)
        button.set_halign(Gtk.Align.CENTER)
        self.no_result_box.pack_start(icon, False, True, 0)
        self.no_result_box.pack_start(label, False, False, 8)
        self.no_result_box.pack_start(button, False, False, 16)
        self.no_result_box.set_valign(Gtk.Align.CENTER)

        self.box.pack_start(self.no_result_box, True, False, 0)

    # noinspection PyUnusedLocal
    def start_discovery(self, widget=None):
        self.show_loading(True)
        MainWindow.run_in_thread(target=self.discovery)

    def start_bulb_connection(self):
        self.show_loading(True, control_only=True)
        MainWindow.run_in_thread(target=self.bulb_connection)

    def bulb_connection(self):
        self.bulb = Bulb(self.bulb_ip)
        self.update_status()
        self.show_loading(False, control_only=True)
        if not self.control_box.get_parent():
            self.box.pack_start(self.control_box, True, True, 0)

    @staticmethod
    def run_in_thread(target, **kwargs):
        thread = threading.Thread(target=target, kwargs=kwargs)
        thread.daemon = True
        thread.start()


class BulbOptionRow(Gtk.ListBoxRow):
    def __init__(self):
        super().__init__()
        self.set_size_request(-1, 48)

    def set_content(self, label: Gtk.Label, control: Gtk.Widget, control_expand: bool = True):
        h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=64)
        self.add(h_box)
        h_box.pack_start(label, False, False, 0)
        h_box.pack_end(control, control_expand, control_expand, 0)
        label.set_margin_start(16)
        control.set_margin_end(16)

        if not control_expand:
            control.set_halign(Gtk.Align.END)
        self.show_all()


win = MainWindow()
win.show_all()
Gtk.main()
