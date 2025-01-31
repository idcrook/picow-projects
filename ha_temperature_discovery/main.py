import errno
import time
import network
import ubinascii
import json
import sys

import asyncio
from ssd1306 import SSD1306_I2C
import onewire
import ds18x20

sys.path.append("third-party")

# Third party libraries
from mqtt_as import MQTTClient, config
from micropython_bmpxxx import bmpxxx

from config import ONEWIRE_CONFIG, I2C_CONFIG, APP_CONFIG, unique_device_identifier
from secrets import WIFI_SSID, WIFI_PASSWORD, MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD



ssid = WIFI_SSID
password = WIFI_PASSWORD

devname = APP_CONFIG.get("device_name", "picow99")

# https://docs.micropython.org/en/latest/library/network.html#network.hostname
network.hostname(devname)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
uid = unique_device_identifier(mac)
print(mac, uid)

# Wait for connect or fail
max_wait = 12
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
