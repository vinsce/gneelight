from gi.repository import GObject

from gi.repository import Gtk


def drop_scroll_event(widget: Gtk.Widget, event):
    GObject.signal_stop_emission_by_name(widget, 'scroll-event')


def dummy_listener(arg1=None, arg2=None, arg3=None):
    pass
