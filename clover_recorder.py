import sys
from ppadb.client import Client as AdbClient
import time


def record_clover_demo(ip):
    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.device(ip)
    if not device:
        print("problem with connection")
        return
    root_dir_name = "/sdcard/demo_clover"
    device.shell("adb shell mkdir {}".format(root_dir_name))
    demo_dir_name = "{}/{}".format(root_dir_name, time.time())
    device.shell("adb shell mkdir {}".format(demo_dir_name))
    counter = 0
    while True:
        screenshot_name = "{}/screenshot_{}.png".format(demo_dir_name, counter)
        device.shell("adb shell screencap -p {}".format(screenshot_name))
        counter+=1
        print("DEBUG SCREENSHOTER : {} was created".format(screenshot_name))

def main(args):
    record_clover_demo(args[1])

if __name__ == '__main__':
    main(sys.argv)
