from gi.repository import Gtk
from gi.repository.Gtk import Orientation


class BulbSelectionWidget(Gtk.MenuButton):
    listener = NotImplemented

    def __init__(self, default_label):
        super().__init__()
        self.default_label = default_label

        self.box = Gtk.Box(orientation=Orientation.HORIZONTAL)
        self.label = Gtk.Label(label=default_label)
        down_arrow = Gtk.Arrow(Gtk.ArrowType.DOWN)
        down_arrow.set_valign(Gtk.Align.BASELINE)

        self.box.pack_start(self.label, False, False, 0)
        self.box.pack_start(down_arrow, False, False, 8)
        self.add(self.box)

        self.box.set_can_focus(False)
        self.box.set_focus_on_click(False)

        self.bulbs_popover = Gtk.Popover()
        self.bulbs_popover_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.bulbs_popover.add(self.bulbs_popover_box)
        self.bulbs_popover.set_position(Gtk.PositionType.BOTTOM)

        self.set_use_popover(True)
        self.set_popover(self.bulbs_popover)

        self.set_sensitive(False)
        self.show_all()

    def fill_popover(self, bulbs, listener):
        self.listener = listener

        for child in self.bulbs_popover_box.get_children():
            self.bulbs_popover_box.remove(child)

        if len(bulbs) == 0:
            self.label.set_label(self.default_label)
            self.set_sensitive(False)
        else:
            group: Gtk.RadioButton = None
            for bulb in bulbs:
                b = Gtk.RadioButton.new_with_label_from_widget(label=bulb.get_bulb_display_text(), radio_group_member=group)
                self.bulbs_popover_box.pack_start(b, False, False, 4)
                b.connect('toggled', self.bulb_clicked)
                if not group:
                    group = b
            group.set_active(True)
            group.toggled()
            self.set_sensitive(True)
        self.bulbs_popover_box.show_all()

    def bulb_clicked(self, button):
        bulb_label = button.get_label()
        self.label.set_label(bulb_label)
        if self.listener:
            self.listener(bulb_label)
        self.bulbs_popover.popdown()
