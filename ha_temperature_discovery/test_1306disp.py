import errno
import time
from machine import Pin, I2C
import network

# import sys

from ssd1306 import SSD1306_I2C

# sys.path.append("/third-party")
# from secrets import WIFI_SSID, WIFI_PASSWORD

ssd1306_width = 128
ssd1306_height = 32

i2c = I2C(0, sda=Pin(4), scl=Pin(5))
display = SSD1306_I2C(ssd1306_width, ssd1306_height, i2c)

display.fill(0)
display.fill_rect(0, 0, 32, 32, 1)
display.fill_rect(2, 2, 28, 28, 0)
display.vline(9, 8, 22, 1)
display.vline(16, 2, 22, 1)
display.vline(23, 8, 22, 1)
display.fill_rect(26, 24, 2, 4, 1)
display.text('MicroPython', 40, 0, 1)
display.text('SSD1306', 40, 12, 1)
display.text('OLED 128x32', 40, 24, 1)
display.show()

time.sleep(7)

# clear screen
display.fill(0)                         # fill entire screen with colour=0
display.show()
