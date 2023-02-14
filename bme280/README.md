# MQTT sensor node with BME280 sensor

A sensor node proof-of-concept for Pico W in MicroPython

![video of display when starting up](bootup.gif)

 - BME280 Temperature / Pressure / Humidity sensor (I2C connection)
 - SSD1306 OLED display (128x32 dots?) (I2C connection)
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
###mip.install("bme280")
mip.install("umqtt.simple")
mip.install("umqtt.robust")
mip.install("ssd1306")
```

### Copy local code

Use our version of `bme280` micropython library.

```shell
mpremote fs cp bme280.py :lib/
```

**Optional: Launch on power-up**

MicroPython will run any script it finds with the name `main.py` at startup. Probably wait on this until you verify it is running properly (see next section)

```shell
mpremote fs cp mqttdisp.py :main.py
```

## Run the examples

### test mqtt config

There is a simple script included that makes a MQTT client call to publish a message. Is intended to make sure your broker is accessible.

```shell
./test_mosq.sh
```

**NOTE**: All of these will require your local wifi network settings to be set in script, and possibly other device-specific changes.


```shell
# test bme280 connection
mpremote run test.py

# test bme280 + OLED
mpremote run test_oled.py

# add mqtt
mpremote run mqtt.py

# altogether now
mpremote run mqttdisp.py
```
