
# convert to Home Assistant MQTT Discovery protocol

 - PicoW on micropython is the device
 - Three DS18B20 temperature probes are the sensors




## Discovery


https://www.home-assistant.io/integrations/mqtt/#single-component-discovery-payload



 - device
   - ids: MAC?
   - name: `picow1`
 - device_class: temperature
 - unique_id: bed # and probe 1-Bus ID?


 entity name `null` can be parent device plus unique_id?



```json
{
  "dev": {
    "ids": "ea334450945afc",
    "name": "Kitchen",
    "mf": "Bla electronics",
    "mdl": "xya",
    "sw": "1.0",
    "sn": "ea334450945afc",
    "hw": "1.0rev2",
  },
  "o": {
    "name":"bla2mqtt",
    "sw": "2.1",
    "url": "https://bla2mqtt.example.com/support",
  },
  "device_class":"temperature",
  "unit_of_measurement":"°C",
  "value_template":"{{ value_json.temperature}}",
  "unique_id":"temp01ae_t",
  "state_topic":"sensorBedroom/state",
  "qos": 2,
}
```

### Discovery Topic


https://www.home-assistant.io/integrations/mqtt/#device-discovery-payload

device with multiple components

```json
{
  "dev": {
    "ids": "ea334450945afc",
    "name": "Kitchen",
    "mf": "Bla electronics",
    "mdl": "xya",
    "sw": "1.0",
    "sn": "ea334450945afc",
    "hw": "1.0rev2",
  },
  "o": {
    "name":"bla2mqtt",
    "sw": "2.1",
    "url": "https://bla2mqtt.example.com/support",
  },
  "cmps": {
    "some_unique_component_id1": {
      "p": "sensor",
      "device_class":"temperature",
      "unit_of_measurement":"°C",
      "value_template":"{{ value_json.temperature}}",
      "unique_id":"temp01ae_t",
    },
    "some_unique_id2": {
      "p": "sensor",
      "device_class":"humidity",
      "unit_of_measurement":"%",
      "value_template":"{{ value_json.humidity}}",
      "unique_id":"temp01ae_h",
    }
  },
  "state_topic":"sensorBedroom/state",
  "qos": 2,
}

```


https://github.com/jramsgz/pico-w-home-assistant/blob/main/lib/makerlab/mlha.py

https://github.com/jramsgz/pico-w-home-assistant/blob/main/projects/climate/code/main.py


```python
  # Discovery packet for Homeassistant
    def publish_config(self, discovery_topic, name, device_type="sensor", device_class=None, unit_of_measurement=None, state_class=None, state_topic="", expire_after=60):
        print("Publishing discovery packet for " + name)
        config_payload = {
            "name": name,
            "state_topic": self.pico_id + state_topic + "/state",
            "availability": [
                {
                    "topic": self.pico_id + "/system/status",
                    "payload_available": "online",
                    "payload_not_available": "offline"
                }
            ],
            "device": {
                "identifiers": self.pico_id,
                "name": self.device_name,
                "manufacturer": "MakerLab",
                "model": "RPI Pico W MLHA",
                "sw_version": "0.2",
                "connections": [ ["ip", self.wlan.ifconfig()[0]], ["mac", ubinascii.hexlify(self.wlan.config('mac')).decode()] ]
            },
            "unique_id": self.pico_id + "-" + discovery_topic,
            "device_class": device_class,
            "value_template": "{{ value_json." + discovery_topic + " }}",
            "unit_of_measurement": unit_of_measurement,
            "state_class": state_class,
            "expire_after": expire_after
        }
```


### Discovery Topic payload



## Availabilty

 - keep-alive (should be longer than measurement / publish interval)
 - last will and testament



# Misc

Add existing MQTT topics as sensors?

https://www.home-assistant.io/integrations/sensor.mqtt/#temperature-and-humidity-sensors


Topic: `office/sensor1`

```json
{
  "temperature": 23.20,
  "humidity": 43.70
}
```

Then use this configuration example to extract the data from the payload:



```json
# Example configuration.yaml entry
mqtt:
  sensor:
    - name: "Temperature"
      state_topic: "office/sensor1"
      suggested_display_precision: 1
      unit_of_measurement: "°C"
      value_template: "{{ value_json.temperature }}"
    - name: "Humidity"
      state_topic: "office/sensor1"
      unit_of_measurement: "%"
      value_template: "{{ value_json.humidity }}"
```

# reading temperature



# Publishing


ensors
Setting up a sensor with multiple measurement values requires multiple consecutive configuration topic submissions.

Configuration topic no1: `homeassistant/sensor/sensorBedroomT/config`
Configuration payload no1:

```json
{
   "device_class":"temperature",
   "state_topic":"homeassistant/sensor/sensorBedroom/state",
   "unit_of_measurement":"°C",
   "value_template":"{{ value_json.temperature}}",
   "unique_id":"temp01ae",
   "device":{
      "identifiers":[
          "bedroom01ae"
      ],
      "name":"Bedroom",
      "manufacturer": "Example sensors Ltd.",
      "model": "Example Sensor",
      "model_id": "K9",
      "serial_number": "12AE3010545",
      "hw_version": "1.01a",
      "sw_version": "2024.1.0",
      "configuration_url": "https://example.com/sensor_portal/config"
   }
}
```

Configuration topic no2: `homeassistant/sensor/sensorBedroomH/config`
Configuration payload no2:

```json
{
   "device_class":"humidity",
   "state_topic":"homeassistant/sensor/sensorBedroom/state",
   "unit_of_measurement":"%",
   "value_template":"{{ value_json.humidity}}",
   "unique_id":"hum01ae",
   "device":{
      "identifiers":[
         "bedroom01ae"
      ]
   }
}
```

The sensor identifiers or connections option allows to set up multiple entities that share the same device.

 Note


If a device configuration is shared, then it is not needed to add all device details to the other entity configs. It is enough to add shared identifiers or connections to the device mapping for the other entity config payloads.

A common state payload that can be parsed with the value_template in the sensor configs:



```json
{
   "temperature":23.20,
   "humidity":43.70
}
```

https://github.com/zeit0dn1/Temp-Sensor/blob/main/main.py

timestamp?

```python
state = b'{"Time":"' + "{:02d}-{:02d}-{}T{:02d}:{:02d}:{:02d}".format(year, month, day, hour, mins, secs) + b'","temperature":"' + str(tempF) + b'"}'
client.publish(pub, state)  #no retain
```

WDT? with asyncio?

```python
from machine import WDT

#set up our watchdog timer to 8.3 sec
# On rp2040 devices, the maximum timeout is 8388 ms.
wdt = WDT(timeout=8300)

#pet the dog
wdt.feed()

while True:
    # sleep for 10 seconds
    time.sleep(5)
    #pet the dog
    wdt.feed()
    time.sleep(5)
```


https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md#38-delay_ms-class

https://gist.github.com/mivade/f4cb26c282d421a62e8b9a341c7c65f6



## python code structure



<https://github.com/Josverl/micropython-p1meter/blob/main/src/config.py>

```
import config as cfg
if cfg.RUN_SIM and not cfg.RUN_SPLITTER:
    from p1meter_sym import P1MeterSIM
```

multiple sensors with "update" support. kinda interesting

https://github.com/DougWilkinson/sensor-mqtt-homeassistant/blob/main/core/config.py

https://github.com/DougWilkinson/sensor-mqtt-homeassistant/blob/main/core/secrets-sample.py


```python
# main.py

import config


# config.py

try:
    import secrets
except KeyboardInterrupt:
    print("c_secrets: Ctrl-C detected")
    raise
except:
    print("Secrets not found!")
    raise

```

secrets

```python
# secrets.py

def version():
    return "vv"

mqttuser = "username"
mqttpass = "pwd"
mqttserver = "192.168.x.x"
custom_topics = ("global/set","global/heartbeat")
hasstopic = "homeassistant"
code_url = "http://nn.nn.nn.nn:80/local/code/"
```



<https://github.com/prairiesnpr/smart_oven/blob/master/constants.py>


<https://github.com/prairiesnpr/rpi_pico_w_PMS7003_mqtt/blob/master/def_secrets.py>

```python
from secrets import WIFI_AP, WIFI_PWD, MQTT_HOST

from constants import (
    SUB_TPC,
    AV_TPC,
    AV_MSG,
    CFG_MSG,
    ID,
    MQTT_PREFIX,
    TMP_ST_TPC,
    MD_ST_TPC,
    MODE_HEAT,
    MODE_OFF,
    START_TMP,
    TMP_CMD_TPC,
    MIN_TEMP,
    MAX_TMP,
    MD_CMD_TPC,
    AV_MODES,
    DEB_TIME,
    TMP_STEP,
    DIR_DWN,
    DIR_UP,
    BTN_DELAY,
    TMP_CUR_TPC,
    CUR_TMP_RD_PER,
    BTN_STEP_DELAY,
    BTN_HT_DELAY,
    BTN_CLD_DELAY,
    V_IN,
    R_TEMP,
    C_F_MULT,
    C_F_OFFSET,
    U16_MAX,
)

from constants import (
    ST_ON_PIN,
    ST_CL_PIN,
    ST_UP_PIN,
    ST_DN_PIN,
    ST_HT_IN_PIN,
    ST_T_AIN_PIN,
    ST_UP_AIN_PIN,
    ST_DN_AIN_PIN,
    CONSIDER_OFF,
)

from constants import KELVIN_C, A, B, C, T_CORR
from constants import FIR_COEFF, FIR_SCALE

# Local configuration
config["ssid"] = WIFI_AP
config["wifi_pw"] = WIFI_PWD
config["server"] = MQTT_HOST

cur_mode = MODE_OFF
cur_set_temp = START_TMP
cur_act_temp = MIN_TEMP  # Need something?
cur_act_temp_raw = 0

disable_in_btn = False


oven_on_btn = Pin(ST_ON_PIN, Pin.OUT)
oven_on_btn.off()
oven_clear_off_btn = Pin(ST_CL_PIN, Pin.OUT)
oven_clear_off_btn.off()
oven_temp_up_btn = Pin(ST_UP_PIN, Pin.OUT)  # is oven on
oven_temp_up_btn.off()
oven_temp_down_btn = Pin(ST_DN_PIN, Pin.OUT)
oven_temp_down_btn.off()
```


## non-micropython

<https://github.com/unixorn/ha-mqtt-discoverable#sensor>
