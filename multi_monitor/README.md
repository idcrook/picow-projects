# MQTT sensor node with multiple DS18B20 sensors

A sensor node proof-of-concept for Pico W in MicroPython

 - Multiple DS18B20 Temperature probe sensors (Dallas Semiconductor 1-wire connection)
 - SSD1306 OLED display (128x64 dots) (I2C connection)
 - Raspberry Pi Pico W

 Also need: Wi-Fi network, MQTT broker configured, jumper cables of various types, solderless breadboard, and a Raspberry Pi Model B or similar connected to picow over USB cable and via serial connection.

Pre-requisites:
 - Recent MicroPython installed on Pico W
 - Raspberry Pi:
   - configured and connected to Pico W on serial terminal connection
   - connected through USB to Pico W (supplies power and can upload code and run REPL)


## Install

**NOTE**: All of these will require your local wifi network settings to be set in script, and possibly other device-specific changes.

### Install libraries

```
mpremote connect /dev/ttyACM0
# ^]

# copy config file to device
mpremote fs cp config.secrets.json :

mpremote run install_using_mip.py
```

This will connect Pico W to your Wi-Fi and run the micropython code (which will download and install the micropython libraries)

```python
import mip
mip.install("upip")
mip.install("urequests")
### supply our own instead # mip.install("bme280")
### mip.install("umqtt.simple")
### mip.install("umqtt.robust")
mip.install("ssd1306")
mip.install("onewire")
mip.install("ds18x20")
mip.install("github:peterhinch/micropython-mqtt")
```


### Async MQTT

<https://github.com/peterhinch/micropython-mqtt>

Now can be installed using `mip`.

**Optional: Launch on power-up**

MicroPython will run any script it finds with the name `main.py` at startup. Probably wait on this until you verify it is running properly (see next section)

```shell
# mpremote fs cp mqttdisp.py :main.py
mpremote fs cp mqtt_as_disp.py :main.py
```

## Run the examples

We assume here that the DS 1-wire and I2C interfaces and devices are working.


```shell
# create config file (edit script or output)
python3 create_cfg.py
cp config.example.json config.secrets.json
# !! EDIT FILE config.secrets.json for your envirnment

# copy config file to device
mpremote fs cp config.secrets.json :

# altogether now
mpremote run mqtt_as_disp.py
```
