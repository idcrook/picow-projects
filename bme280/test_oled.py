from machine import Pin, I2C        # importing relevant modules & classes
from time import sleep
import bme280
from ssd1306 import SSD1306_I2C


I2C_BME280_ADDRESS = 0x77
I2C_SSD1306_ADDRESS = 0x3c

#i2c=I2C(0, sda=Pin(17), scl=Pin(16), freq=400000)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
display = SSD1306_I2C(128, 32, i2c, addr=I2C_SSD1306_ADDRESS)

display.fill(0)
display.text('MicroPython', 40, 0, 1)
display.text('SSD1306', 40, 12, 1)
display.text('OLED 128x32', 40, 24, 1)

display.show()
# sleep(2)
bme = bme280.BME280(i2c=i2c, address=I2C_BME280_ADDRESS)

while True:
    print(bme.values)
    display.fill(0)
    display.text("Temp " + bme.values[0], 3, 0, 1)
    display.text("PA  " + bme.values[1], 3, 11, 1)
    display.text("Humidity " + bme.values[2], 3, 23, 1)
    display.show()
    sleep(10)                                        # delay of 10s
