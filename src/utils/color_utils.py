from gi.overrides.Gdk import RGBA


def parse_rgb(rgb):
    r = int(rgb / 65536) / 255
    rgb = rgb % 65536
    g = int(rgb / 256) / 255
    rgb = rgb % 256
    b = rgb / 255
    return RGBA(red=r, green=g, blue=b)
