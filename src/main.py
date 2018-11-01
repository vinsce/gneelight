from gi.overrides.Gdk import RGBA

import gi
from BulbWrapper import BulbWrapper
from constants import *
from utils.color_utils import parse_rgb

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


# TODO add predefined options
# TODO add bulb info section


# noinspection PyArgumentList
class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, *args, **kwargs)

        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(400, 400)

        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = APP_NAME
        self.set_titlebar(self.header_bar)
        self.set_hide_titlebar_when_maximized(False)
        self.set_decorated(True)
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

        self.discovered_bulbs = []
        self.bulb_wrapper: BulbWrapper = None

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

        row3 = BulbOptionRow()
        self.delay_spin_button = Gtk.SpinButton.new_with_range(min=0, max=60, step=1)
        self.delay_spin_button.connect('value-changed', self.change_delay_off)
        row3.set_content(Gtk.Label(label="Delay off (minutes)", xalign=0), self.delay_spin_button, control_expand=False)
        self.control_box.add(row3)

        row4 = BulbOptionRow()
        self.color_button = Gtk.ColorButton.new_with_rgba(rgba=RGBA())
        self.color_button.connect('color-set', self.change_color)
        row4.set_content(Gtk.Label(label="Color", xalign=0), self.color_button, control_expand=False)
        self.control_box.add(row4)

    # noinspection PyUnusedLocal
    def toggle_bulb(self, widget, status):
        self.bulb_wrapper.toggle(status=status, on_complete=self.update_status_on_complete)

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

    def discovered(self, wrappers):
        self.discovered_bulbs = wrappers

        self.show_loading(False)

        if len(self.discovered_bulbs) > 0:
            self.bulbs_combo.remove_all()

            for bulb in self.discovered_bulbs:
                self.bulbs_combo.append_text(bulb.get_bulb_display_text())
                print(bulb)

            self.box.pack_start(self.bulbs_combo, False, False, 6)
            self.bulbs_combo.set_active(0)
        else:
            self.show_no_result()
        self.box.show_all()

    def on_bulb_selected(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()

            for bw in self.discovered_bulbs:
                if bw.get_bulb_display_text() == model[tree_iter][0]:
                    self.bulb_wrapper = bw

            print("Selected: bulb=%s" % self.bulb_wrapper.get_bulb_display_text())

            self.show_loading(True, control_only=True)
            self.bulb_wrapper.update_status(on_complete=self.bulb_connected)
        else:
            pass

    # noinspection PyUnusedLocal
    def change_brightness(self, widget, event):
        bright = self.brightness_slider.get_value()
        self.bulb_wrapper.change_brightness(bright, self.update_status_on_complete)

    # noinspection PyTypeChecker,PyUnusedLocal
    def change_color(self, widget):
        self.bulb_wrapper.change_color(self.color_button.get_rgba(), self.update_status_on_complete)

    # noinspection PyUnusedLocal
    def change_delay_off(self, widget):
        self.bulb_wrapper.change_delay_off(delay=self.delay_spin_button.get_value(), on_complete=self.update_status_on_complete)

    def update_status(self):
        self.bulb_wrapper.update_status(self.update_status_on_complete)

    def update_status_on_complete(self):
        self.power_switch.set_active(self.bulb_wrapper.bulb_status.power == 'on')
        self.brightness_slider.set_value(self.bulb_wrapper.bulb_status.bright)
        self.delay_spin_button.set_value(self.bulb_wrapper.bulb_status.delay_off)
        if self.bulb_wrapper.bulb_status.rgb:
            self.color_button.set_rgba(parse_rgb(self.bulb_wrapper.bulb_status.rgb))
        else:
            self.color_button.set_rgba(RGBA())

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
        BulbWrapper.discovery_bulbs(on_complete=self.discovered)

    def bulb_connected(self):
        self.update_status_on_complete()
        self.show_loading(False, control_only=True)
        if not self.control_box.get_parent():
            self.box.pack_start(self.control_box, True, True, 0)


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
