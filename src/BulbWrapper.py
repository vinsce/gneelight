from gi.overrides.Gdk import RGBA
from yeelight import Bulb, discover_bulbs
from yeelight.enums import CronType

from gi.repository.GLib import idle_add
from utils.thread_utils import run_in_thread


class BulbStatus:
    def __init__(self, bulb_status):
        self.power = bulb_status.get('power')
        self.bright = int(bulb_status.get('bright')) if bulb_status.get('bright') else None
        self.color_mode = int(bulb_status.get('color_mode'))
        self.ct = int(bulb_status.get('ct')) if bulb_status.get('ct') else None
        self.rgb = int(bulb_status.get('rgb')) if bulb_status.get('rgb') else None
        self.hue = int(bulb_status.get('hue')) if bulb_status.get('hue') else None
        self.sat = int(bulb_status.get('sat')) if bulb_status.get('sat') else None
        self.name = bulb_status.get('name')
        self.delay_off = int(bulb_status.get('delayoff')) if bulb_status.get('delayoff') else None


class BulbWrapper:
    def __init__(self, bulb_info):
        self.bulb_ip = bulb_info.get('ip')
        self.bulb_port = bulb_info.get('port')
        self.bulb_model = bulb_info.get('capabilities').get('model')
        self.bulb_fw_version = bulb_info.get('capabilities').get('fw_ver')
        self.bulb_support = bulb_info.get('capabilities').get('support').split(' ')
        self.bulb_status = BulbStatus(bulb_info.get('capabilities'))
        self.bulb: Bulb = None

    def get_bulb_display_text(self):
        return self.bulb_ip + ":" + str(self.bulb_port) + ' (' + self.bulb_model + ')'

    def get_bulb(self):
        if not self.bulb:
            self.bulb = Bulb(self.bulb_ip)
        return self.bulb

    # Status update
    def update_status(self, on_complete=None):
        run_in_thread(target=self.update_status_sync, on_complete=on_complete)

    def update_status_sync(self, on_complete=None):
        self.bulb_status = BulbStatus(self.get_bulb().get_properties())
        if on_complete:
            idle_add(on_complete)

    # Brightness
    def change_brightness(self, brightness, on_complete):
        run_in_thread(target=self.change_brightness_sync, brightness=brightness, on_complete=on_complete)

    def change_brightness_sync(self, brightness, on_complete):
        self.get_bulb().set_brightness(brightness=brightness)
        self.update_status_sync()
        idle_add(on_complete)

    # Color
    def change_color(self, color: RGBA, on_complete):
        run_in_thread(target=self.change_color_sync, color=color, on_complete=on_complete)

    def change_color_sync(self, color: RGBA, on_complete):
        self.get_bulb().set_rgb(red=color.red * 255, green=color.green * 255, blue=color.blue * 255)
        self.update_status_sync()
        idle_add(on_complete)

    # Delay off
    def change_delay_off(self, delay, on_complete):
        run_in_thread(target=self.change_delay_off_sync, delay=delay, on_complete=on_complete)

    def change_delay_off_sync(self, delay, on_complete):
        if delay == 0:
            self.get_bulb().cron_del(CronType.off)
        else:
            self.get_bulb().cron_add(CronType.off, delay)
        self.update_status_sync()
        idle_add(on_complete)

    # Toggle
    def toggle(self, status, on_complete):
        run_in_thread(target=self.toggle_sync, status=status, on_complete=on_complete)

    def toggle_sync(self, status, on_complete):
        if status:
            self.get_bulb().turn_on()
        else:
            self.get_bulb().turn_off()
        self.update_status_sync()
        idle_add(on_complete)

    @staticmethod
    def discovery_bulbs(on_complete):
        run_in_thread(target=BulbWrapper.discovery_bulbs_sync, on_complete=on_complete)

    @staticmethod
    def discovery_bulbs_sync(on_complete):
        discovered_bulbs = discover_bulbs()

        wrappers = []
        for bulb_info in discovered_bulbs:
            wrappers.append(BulbWrapper(bulb_info))
        idle_add(on_complete, wrappers)
