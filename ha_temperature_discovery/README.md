# Home Assistant Temperature Sensor

Micropython Home Assistant sensor driver

## Features

 - Uses micropython and `asyncio`/`mqtt_as` for reliability and performance.
 - Can handle network downtimes and flakiness
   - Has hardware watchdog timer (WDT) support
 - Integrates into local `MQTT` and supports MQTT Discovery for sensors in Home Assistant

## Requirements

 - Pico W microcontroller board, connecting to WiFi.
   - Up to three DS18B20 1-wire temperature probes connected
   - (Optional) OLED matrix (using I2C) for displaying info
   - (Optional) BM[EP] sensor (using I2C) for ambient condiditions
 - Home Assistant with MQTT integration


### micropython target setup

Assumes  [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html) is installed in macOS (host) and recent version of micropython (target).

I use macOS or Linux, and am targetting Raspberry Pi Pico W.


```shell
❯ mpremote connect /dev/tty.usbmodem33101
python-repl
Connected to MicroPython at /dev/cu.usbmodem33101
Use Ctrl-] or Ctrl-x to exit this shell

>>>
```

### mip

like `pip` for micropython

```shell
# set up for your wi-fi, and then copy over
mpremote fs cp secrets.py :
mpremote run mip_install.py
```


## Putting on Pico W


```shell
# customize these before copying
mpremote fs cp secrets.py :
mpremote fs cp config-picow1.py :config.py
mpremote fs cp device-picow1.py :device.py

# testing
mpremote run test_ds18b20.py
mpremote run main.py
```


To have it launch on "boot up", copy `main.py` to Pico W storage. `micropython` will run it after reset.
