from gi.repository import Gtk, Gio


class MenuWidget(Gtk.MenuButton):

    def __init__(self, window, listener):
        super().__init__()

        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.add(image)

        self.menu_popover = Gtk.Popover()
        self.menu_popover_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.menu_popover.add(self.menu_popover_box)
        self.menu_popover.set_position(Gtk.PositionType.BOTTOM)

        self.set_use_popover(True)

        self.show_all()

        self.listener = listener
        menumodel = Gio.Menu()
        menumodel.append("Settings", "win.settings")
        menumodel.append("About", "win.about")

        self.set_menu_model(menumodel)

        self.menu_popover_box.show_all()

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.item_clicked)
        window.add_action(about_action)

        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.item_clicked)
        window.add_action(settings_action)

    def item_clicked(self, b: Gio.SimpleAction, e):
        self.listener(b.get_name())
