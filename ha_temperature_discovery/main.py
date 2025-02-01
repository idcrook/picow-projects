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
from machine import Pin, I2C

# Third party libraries
sys.path.append("/third-party")
from mqtt_as import MQTTClient, config
from micropython_bmpxxx import bmpxxx

from config import ONEWIRE_CONFIG, I2C_CONFIG, APP_CONFIG, unique_device_identifier
from secrets import WIFI_SSID, WIFI_PASSWORD, MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD

ssid = WIFI_SSID
password = WIFI_PASSWORD
DEVNAME = APP_CONFIG.setdefault("device_name", "picow999")

# https://docs.micropython.org/en/latest/library/network.html#network.hostname
network.hostname(DEVNAME)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

mac = binascii.hexlify(network.WLAN().config('mac'),':').decode()
udi = unique_device_identifier(mac)

# use name and unique device ID to generate if not specified
UNIQ_ID_PRE_ = APP_CONFIG.setdefault("unique_id", f"{DEVNAME}_{udi}_")
print(DEVNAME, mac, udi, UNIQ_ID_PRE_)

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

# 1-wire configs
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

if True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)

    try:
        for s_id, s_params in found_sensors.items():
            device = s_params['device']
            temperature = round(ds_sensor.read_temp(device), 1)
            print(s_id, temperature, "C")
    except OneWireError as error:
        print("error with", device)
        print(error)
        # FIXME: hopefully a transient issue but add better handling
        pass

# I2C configs
i2c_bus_info = I2C_CONFIG['bus']
i2c_bus = i2c_bus_info['bus_number']
i2c_sda = Pin(i2c_bus_info['sda_pin'])
i2c_scl = Pin(i2c_bus_info['scl_pin'])

i2c = I2C(i2c_bus, sda=i2c_sda, scl=i2c_scl)

# I2C sensors config - bme280
I2C_SENSORS = []
I2C_SENSORS_FOUND = False
for sensor in I2C_CONFIG.get('sensors', []):
    I2C_SENSORS_FOUND = True
    for s_type, s_params in sensor.items():
        if s_type == 'bme280':
            address = s_params.setdefault('address', 0x77)
            # FIXME: Handle RuntimeError if not found, e.g.
            # RuntimeError: BME280 sensor not found at specified I2C address (0x77).
            this = bmpxxx.BME280(i2c, address=address)
            info = {}
            info['device_type'] = s_type
            info['address'] = address
            info['interface'] = this
            I2C_SENSORS.append(info)

if I2C_SENSORS_FOUND:
    #print(I2C_SENSORS)
    for i2c_sensor in I2C_SENSORS:
        sensor_interface = i2c_sensor['interface']
        name = i2c_sensor['device_type']
        if name == 'bme280':
            temperature = sensor_interface.temperature
            humidity = sensor_interface.humidity
            dewpoint = sensor_interface.dew_point
            print(f"{name}:> {temperature:.1f}C rel humid:{humidity:.1f}% dewpt:{dewpoint:.1f}C")

# I2C displays config
I2C_DISPLAYS = []
I2C_DISPLAYS_FOUND = False
i2c_displays = I2C_CONFIG.get('displays', [])

# assume zero or one (no more) display for now
if len(i2c_displays):
    display_info = i2c_displays[0]
    #print(display_info)
    for d_type, d_params in display_info.items():
        address = d_params['address']
        h = d_params['height']
        w = d_params['width']
        display = SSD1306_I2C(w, h, i2c)
        display.fill(0)
        display.text(DEVNAME, 0, 0, 1)
        display.text(UNIQ_ID_PRE_, 0, 12, 1)
        display.show()
        info = {'device_type': d_type, 'interface': display }
        info.update(d_params)
        I2C_DISPLAYS_FOUND = True
        I2C_DISPLAYS.append(info)

print("displays found:", I2C_DISPLAYS)
if I2C_DISPLAYS_FOUND:
    time.sleep(7)
    I2C_DISPLAYS[0]['interface'].fill(0)
    I2C_DISPLAYS[0]['interface'].show()
