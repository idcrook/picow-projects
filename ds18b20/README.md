# MQTT sensor node with BME280 sensor

A sensor node proof-of-concept for Pico W in MicroPython

 - DS18B20 Temperature probe (waterproof)

 
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
mip.install("onewire")
mip.install("ds18x20")
```


## Run the examples

```shell
# test DS18B20 connection and function
mpremote run test.py
```
