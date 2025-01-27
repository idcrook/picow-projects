# Home Assistant Temperature Sensor

Uses MQTT Discovery protocol.

# Requirements

 - Pico W microcontroller board, connecting to WiFi.
   - Up to three DS18B20 1-wire temperature probes connected
   - (Optional) OLED matrix (using I2C) for displaying info
   - (Optional) BMP* sensor (using I2C) for ambient condiditions
 - Home Assistant with MQTT integration


## micropython target setup

Assumes `mpremote` is installed in macOS (host) and recent version of micropython (target).

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
mpremote fs cp secrets.py :
mpremote run mip_install.py
```
