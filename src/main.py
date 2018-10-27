import threading

import gi
from yeelight import discover_bulbs, Bulb

from src.constants import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=APP_NAME)
        self.connect("destroy", Gtk.main_quit)
        self.resize(400, 400)

        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)

        self.spinner = Gtk.Spinner()

        self.show_loading(True)

        self.bulbs_combo = Gtk.ComboBoxText()
        self.bulbs_combo.set_entry_text_column(0)
        self.bulbs_combo.connect("changed", self.on_bulb_selected)

        self.discovered_bulbs = None
        self.bulb_ip = None
        self.bulb = None

        self.show_all()

        self.init_control_layout()

        thread = threading.Thread(target=self.discovery)
        thread.daemon = True
        thread.start()

    def init_control_layout(self):
        self.control_box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)

        self.status_label = Gtk.Label()
        self.toggle_button = Gtk.Button(label="Toggle")
        self.toggle_button.connect("clicked", self.toggle_bulb)
        self.control_box.pack_start(self.status_label, False, False, 0)
        self.control_box.pack_start(self.toggle_button, False, False, 0)

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
            self.spinner.start()
            self.box.pack_start(self.spinner, True, True, 0)
        else:
            self.spinner.stop()
            self.box.remove(self.spinner)

    def discovery(self):
        self.discovered_bulbs = discover_bulbs()

        for bulb in self.discovered_bulbs:
            self.bulbs_combo.append_text(bulb.get('ip') + ":" + str(bulb.get('port')))

        self.show_loading(False)

        self.box.pack_start(self.bulbs_combo, False, False, 4)
        self.box.pack_start(self.control_box, True, True, 0)
        self.show_all()

    def on_bulb_selected(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.bulb_ip = model[tree_iter][0].split(':')[0]
            print("Selected: bulb=%s" % self.bulb_ip)
            self.bulb = Bulb(self.bulb_ip)
            self.update_status()

    def update_status(self):
        self.status_label.set_text('Status: ' + self.bulb.get_properties().get('power'))


win = MainWindow()
Gtk.main()
