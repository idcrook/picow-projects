import errno
import time
import network

import json
import sys


# from secrets import WIFI_SSID, WIFI_PASSWORD, MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD
from secrets import WIFI_SSID, WIFI_PASSWORD


ssid = WIFI_SSID
password = WIFI_PASSWORD

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
# mip.install("upip")
mip.install("requests")
# mip.install("umqtt.simple")
# mip.install("umqtt.robust")
mip.install("ssd1306")
mip.install("onewire")
mip.install("ds18x20")
mip.install("github:peterhinch/micropython-mqtt", target="third-party")
mip.install("github:idcrook/micropython-tomli", target="third-party")

sys.path.append("third-party")

# test local installation
import asyncio
from ssd1306 import SSD1306_I2C
import onewire
import ds18x20
import json
from mqtt_as import MQTTClient, config
import tomli
