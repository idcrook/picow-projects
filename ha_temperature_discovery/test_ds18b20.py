from machine import Pin
from time import sleep, sleep_ms
import binascii
import onewire
import ds18x20

# https://picow.pinout.xyz/ "GP22" -> row 12 on breadboard
ONEWIRE_DATA_PIN = 22

ds_pin = Pin(ONEWIRE_DATA_PIN)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
for device in roms:
    s = binascii.hexlify(device)
    readable_string = s.decode('ascii')
    print(readable_string)


while True:
    ds_sensor.convert_temp()
    # sleep(2)
    sleep_ms(750)
    for rom in roms:
        temperature = round(ds_sensor.read_temp(rom), 1)
        print(temperature, "C")
    sleep(5)
