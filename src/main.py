import threading

from yeelight import discover_bulbs, Bulb

import gi
from constants import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


# TODO add predefined options
# TODO add bulb info section
# TODO add delay off option


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

        self.start_discovery()

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

    def toggle_bulb(self, widget, status):
        if status:
            self.bulb.turn_on()
        else:
            self.bulb.turn_off()
        self.update_status()

    def on_button_clicked(self, widget):
        print(self.bulb.get_properties())
        if self.bulb.get_properties().get('power') == 'on':
            self.bulb.turn_off()
        else:
            self.bulb.turn_on()

    def show_loading(self, loading):
        if loading:
            self.box.remove(self.bulbs_combo)
            self.box.remove(self.control_box)
            for child in self.box.get_children():
                self.box.remove(child)
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

            self.bulbs_combo.set_active(0)

            self.box.pack_start(self.bulbs_combo, False, False, 6)
            self.box.pack_start(self.control_box, True, True, 0)
        else:
            self.show_no_result()
        self.box.show_all()

    def on_bulb_selected(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.bulb_ip = model[tree_iter][0].split(':')[0]
            print("Selected: bulb=%s" % self.bulb_ip)
            self.bulb = Bulb(self.bulb_ip)
            self.update_status()
        else:
            pass

    def change_brightness(self, widget, event):
        bright = self.brightness_slider.get_value()
        self.bulb.set_brightness(bright)
        self.update_status()

    def update_status(self):
        bulb_properties = self.bulb.get_properties()
        print(bulb_properties)

        self.power_switch.set_active(bulb_properties.get('power') == 'on')
        self.brightness_slider.set_value(int(bulb_properties.get('bright')))
        self.control_box.show_all()

    def show_no_result(self):
        no_result_box = Gtk.VBox(homogeneous=False)

        pixbuf = Gtk.IconTheme.get_default().load_icon('computer-fail-symbolic', 64, 0)

        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        label = Gtk.Label(label='No bulb found')
        button = Gtk.Button(label='Retry')
        button.connect("clicked", self.start_discovery)
        button.set_hexpand(False)
        button.set_halign(Gtk.Align.CENTER)
        no_result_box.pack_start(icon, False, True, 0)
        no_result_box.pack_start(label, False, False, 8)
        no_result_box.pack_start(button, False, False, 16)
        no_result_box.set_valign(Gtk.Align.CENTER)

        self.box.pack_start(no_result_box, True, False, 0)

    def start_discovery(self, widget=None):
        self.show_loading(True)

        thread = threading.Thread(target=self.discovery)
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
