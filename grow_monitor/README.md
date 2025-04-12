IMPORTANT: This project lives on in own repository. Preserved here for historical reason.

For the repo: <https://github.com/idcrook/yaha_temperature_monitor>

# MQTT sensor node with DS18B20 and BME280 sensor

A sensor node proof-of-concept for Pico W in MicroPython

 - DS18B20 Temperature probe sensor (Dallas Semiconductor 1-wire connection)
 - BME280 Temperature / Pressure / Humidity sensor (I2C connection)
 - SSD1306 OLED display (128x32? dots) (I2C connection)
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
mpremote run install_using_mip.py
```

This will connect Pico W to your Wi-Fi and run the micropython code (which will download and install the micropython libraries)

```python
mip.install("upip")
mip.install("urequests")
### supply our own instead # mip.install("bme280")
### mip.install("umqtt.simple")
### mip.install("umqtt.robust")
mip.install("ssd1306")
mip.install("onewire")
mip.install("ds18x20")
```


Async MQTT

https://github.com/peterhinch/micropython-mqtt/blob/master/mqtt_as/README.md

```
wget https://raw.githubusercontent.com/peterhinch/micropython-mqtt/master/mqtt_as/mqtt_as.py
```

### Copy local code

Use our version of `bme280` micropython library and the `mqtt_as` library.

```shell
mpremote fs cp bme280.py :lib/
mpremote fs cp mqtt_as.py :lib/
```

**Optional: Launch on power-up**

MicroPython will run any script it finds with the name `main.py` at startup. Probably wait on this until you verify it is running properly (see next section)

```shell
# mpremote fs cp mqttdisp.py :main.py
mpremote fs cp mqtt_as_disp.py :main.py
```

## Run the examples

See the `bme280` example directory for progressive feature troubleshooting. We assume here that the DS 1-wire and I2C interfaces and devices are working.


```shell
# create config file (edit script or output)
python3 create_cfg.py
copy config.example.json config.secrets.json
# !! EDIT FILE config.secrets.json for your envirnment

# copy config file to device
mpremote fs cp config.secrets.json :

# altogether now
mpremote run mqttdisp.py
```
