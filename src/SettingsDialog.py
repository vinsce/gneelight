from constants import APP_ID
from gi.repository import Gtk, Gio
from gi.repository.Gtk import HBox, VBox


class SettingsDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, parent=parent)
        self.set_title("Settings")
        self.set_default_size(450, 300)
        box = self.get_content_area()
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(16)
        box.set_margin_bottom(16)

        app_indicator_row = HBox()
        app_indicator_details_box = VBox()
        app_indicator_label = Gtk.Label(xalign=0)
        app_indicator_label.set_markup("<b>Enable AppIndicator</b>")
        app_indicator_description_label = Gtk.Label(xalign=0, label="Minimize the application to AppIndicator when the close button is pressed, if connected to a bulb.")
        app_indicator_description_label.set_line_wrap(True)
        app_indicator_details_box.pack_start(app_indicator_label, False, False, 0)
        app_indicator_details_box.pack_start(app_indicator_description_label, False, False, 0)

        app_indicator_switch = Gtk.Switch()

        app_indicator_row.pack_start(app_indicator_details_box, True, True, 8)
        app_indicator_row.pack_end(app_indicator_switch, False, False, 0)

        app_indicator_switch.set_vexpand(False)
        app_indicator_switch.set_valign(Gtk.Align.CENTER)

        box.pack_start(app_indicator_row, False, False, 0)

        settings = Gio.Settings(APP_ID)
        settings.bind('enable-appindicator', app_indicator_switch, 'active', Gio.SettingsBindFlags.DEFAULT)

        self.show_all()
