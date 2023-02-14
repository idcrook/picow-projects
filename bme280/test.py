from machine import Pin, I2C
from time import sleep
import bme280

I2C_BME280_ADDRESS = 0x77

#i2c=I2C(0, sda=Pin(17), scl=Pin(16), freq=400000)    # initializing the I2C method
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)    # initializing the I2C method

# i2c.scan() can be handy to determine device address

while True:
    bme = bme280.BME280(i2c=i2c, address=I2C_BME280_ADDRESS)
    print(bme.values)
    sleep(10)                                        # delay of 10s
