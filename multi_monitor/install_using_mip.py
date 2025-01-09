import errno
import time
import network

import json
# from mqtt_as import MQTTClient, config


CONFIG_FILE = 'config.secrets.json'

DEFAULT_WIFI_SSID = "Guest"
DEFAULT_WIFI_PASSWORD = "password"

CONFIG = {}

try:
    with open(CONFIG_FILE, 'r') as jsonfile:
        CONFIG = json.loads(jsonfile.read())
        print(CONFIG)
except OSError as ose:
    if ose.errno not in (errno.ENOENT,):
        # this re-raises the same error object.
        raise

# subtrees of the config file
WIFI_CONF = CONFIG.get("wifi", {})

wifi_ssid = WIFI_CONF.get('ssid', DEFAULT_WIFI_SSID)
wifi_password = WIFI_CONF.get('password', DEFAULT_WIFI_PASSWORD)
# config['ssid'] = wifi_ssid
# config['wifi_pw'] = wifi_password


ssid = wifi_ssid
password = wifi_password


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:

    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')

status = wlan.ifconfig()
print('ip = ' + status[0])

import mip
mip.install("upip")
mip.install("urequests")
# mip.install("umqtt.simple")
# mip.install("umqtt.robust")
mip.install("ssd1306")
mip.install("onewire")
mip.install("ds18x20")
mip.install("github:peterhinch/micropython-mqtt")
