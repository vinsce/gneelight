import threading

import gi
from yeelight import discover_bulbs, Bulb

from constants import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=APP_NAME)
        self.connect("destroy", Gtk.main_quit)
        self.resize(400, 400)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)

        self.spinner = Gtk.Spinner()

        self.bulbs_combo = Gtk.ComboBoxText()
        self.bulbs_combo.set_entry_text_column(0)
        self.bulbs_combo.connect("changed", self.on_bulb_selected)
        self.bulbs_combo.set_hexpand(False)
        self.bulbs_combo.set_halign(Gtk.Align.CENTER)

        self.discovered_bulbs = None
        self.bulb_ip = None
        self.bulb = None

        self.init_control_layout()

        self.show_loading(True)
        self.show_all()

        thread = threading.Thread(target=self.discovery)
        thread.daemon = True
        thread.start()

    def init_control_layout(self):
        self.control_box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.control_box.set_margin_start(16)
        self.control_box.set_margin_end(16)

        self.status_label = Gtk.Label()
        self.toggle_button = Gtk.Button(label="Toggle")
        self.toggle_button.connect("clicked", self.toggle_bulb)
        self.control_box.pack_start(self.status_label, False, False, 0)
        self.control_box.pack_start(self.toggle_button, False, False, 0)

        self.brightness_slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,
                                           adjustment=Gtk.Adjustment(lower=1, upper=100, step_increment=1))
        self.control_box.pack_start(self.brightness_slider, False, False, 0)
        self.brightness_slider.connect("button-release-event", self.change_brightness)

    def toggle_bulb(self, widget):
        self.bulb.toggle()
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
            self.spinner.start()
            self.box.pack_start(self.spinner, True, True, 150)
        else:
            self.spinner.stop()
            self.box.remove(self.spinner)

    def discovery(self):
        self.discovered_bulbs = discover_bulbs()

        for bulb in self.discovered_bulbs:
            self.bulbs_combo.append_text(bulb.get('ip') + ":" + str(bulb.get('port')))
        self.bulbs_combo.set_active(0)

        self.show_loading(False)

        self.box.pack_start(self.bulbs_combo, False, False, 6)
        self.box.pack_start(self.control_box, True, True, 0)
        self.show_all()

    def on_bulb_selected(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None and len(tree_iter)!=0:
            model = combo.get_model()
            self.bulb_ip = model[tree_iter][0].split(':')[0]
            print("Selected: bulb=%s" % self.bulb_ip)
            self.bulb = Bulb(self.bulb_ip)
            self.update_status()
        else:
            # TODO show message to user
            pass

    def change_brightness(self, widget, event):
        bright = self.brightness_slider.get_value()
        self.bulb.set_brightness(bright)
        self.update_status()

    def update_status(self):
        bulb_properties = self.bulb.get_properties()
        print(bulb_properties)

        self.status_label.set_text('Status: ' + bulb_properties.get('power'))
        self.brightness_slider.set_value(int(bulb_properties.get('bright')))


win = MainWindow()
Gtk.main()
