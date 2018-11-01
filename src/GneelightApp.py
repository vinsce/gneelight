import gi, sys
from constants import APP_NAME, AUTHORS, WEBSITE, APP_VERSION, APP_COMMENTS
from gi.repository.Gio import MenuModel
from main import MainWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

# This would typically be its own file
MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""


class GneelightApp(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="me.vinsce.Gneelight", flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        # noinspection PyTypeChecker
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = MainWindow(application=self, title=APP_NAME)

        self.window.show_all()

    # noinspection PyArgumentList
    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.set_authors(AUTHORS)
        about_dialog.set_program_name(APP_NAME)
        about_dialog.set_website(WEBSITE)
        about_dialog.set_comments(APP_COMMENTS)
        about_dialog.set_version(APP_VERSION)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = GneelightApp()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
