import errno
import time
import network

import json
import sys


# from secrets import WIFI_SSID, WIFI_PASSWORD, MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD
from secrets import WIFI_SSID, WIFI_PASSWORD
sys.path.append("third-party")


from machine import Pin, I2C


# # test local installation
# import asyncio
# from ssd1306 import SSD1306_I2C
# import onewire
# import ds18x20
# import json
# from mqtt_as import MQTTClient, config
# import tomli
from micropython_bmpxxx import bmpxxx


i2c = I2C(0, sda=Pin(4), scl=Pin(5))
bmp = bmpxxx.BMP280(i2c, address=0x77)

temp = bmp.temperature
print(temp)

did = bmp._read_device_id()
print(did, f"{did:#x}")
