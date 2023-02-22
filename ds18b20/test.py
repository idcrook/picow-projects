from machine import Pin
from time import sleep, sleep_ms
import onewire, ds18x20

ONEWIRE_DATA_PIN = 26


ds_pin = Pin(ONEWIRE_DATA_PIN)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()

while True:
    ds_sensor.convert_temp()
    #sleep(2)
    sleep_ms(750)
    for rom in roms:
        temperature = round(ds_sensor.read_temp(rom),1)
        print(temperature, "C")
    sleep(5)