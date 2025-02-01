import errno
import time
import network
import binascii
import json
import sys

import asyncio
import ds18x20
import onewire
from onewire import OneWireError
from ssd1306 import SSD1306_I2C
from machine import Pin

# Third party libraries
sys.path.append("third-party")
from mqtt_as import MQTTClient, config
from micropython_bmpxxx import bmpxxx

from config import ONEWIRE_CONFIG, I2C_CONFIG, APP_CONFIG, unique_device_identifier
from secrets import WIFI_SSID, WIFI_PASSWORD, MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD



ssid = WIFI_SSID
password = WIFI_PASSWORD

devname = APP_CONFIG.setdefault("device_name", "picow999")

# https://docs.micropython.org/en/latest/library/network.html#network.hostname
network.hostname(devname)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

mac = binascii.hexlify(network.WLAN().config('mac'),':').decode()
udi = unique_device_identifier(mac)

# use name and unique device ID to generate if not specified
UNIQ_ID_PRE_ = APP_CONFIG.setdefault("unique_id", f"{devname}_{udi}_")
print(devname, mac, udi, UNIQ_ID_PRE_)

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


ds_pin = Pin(ONEWIRE_CONFIG.get("data_pin", 22))
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
#print (roms)

sensors = ONEWIRE_CONFIG.get("sensors", {})
#print(sensors)
found_sensors = {}

for device in roms:
    s = binascii.hexlify(device)
    readable_string = s.decode('ascii')
    #print(readable_string)
    if readable_string in sensors:
        info = {}
        info['name'] = sensors[readable_string]['name']
        info['device'] = device
        found_sensors[readable_string] = info


print ("found 1-wire", found_sensors)

while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)

    try:
        for s_id, s_params in found_sensors.items():
            device = s_params['device']
            temperature = round(ds_sensor.read_temp(device), 1)
            print(s_id, temperature, "C")
    except OneWireError:
        # FIXME: hopefully a transient issue but add better handling
        pass
