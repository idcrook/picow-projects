
# convert to Home Assistant MQTT Discovery protocol

 - PicoW on micropython is the device
 - Three DS18B20 temperature probes are the sensors




## Discovery


 <https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery>
 <https://www.home-assistant.io/integrations/mqtt/#configuration-via-mqtt-discovery>
 <https://www.home-assistant.io/integrations/sensor.mqtt/>
 <https://www.home-assistant.io/integrations/sensor.mqtt/#temperature-and-humidity-sensors>

 Outline of Home Assistant MQTT discovery for sensor

### Discovery messages


Configuration topic no1: homeassistant/sensor/picow0_940/abcd/config
Configuration topic no2: homeassistant/sensor/picow0_940/abd1/config
Configuration topic no3: homeassistant/sensor/picow0_940/abd2/config
Configuration topic no4: homeassistant/sensor/picow0_940/abd4/config
Configuration topic no5: homeassistant/sensor/picow0_940/bmeT/config
Configuration topic no6: homeassistant/sensor/picow0_940/bmeH/config

state topic (shared):    homeassistant/sensor/picow0_940/state

```javascript
{
  "stat_t": "home/sensor/picow0_940/state",
  "name": "picow0_940-bed1_temp",
  "uniq_id": "picow0_940-abcd-bed1_temp",
  "dev_cla": "temperature",
  "val_tpl": "{{ value_json.bed1_temperature | is_defined }}",
  "unit_of_meas": "F",
  "device": {
    "name": "picow0_940",
    "manufacturer": "idcrook-labs",
    "model": "seed-o-matic",
    "model_id": "K9",
    "serial_number": "MACADDR",
    "hw_version": "1.01a",
    "sw_version": "2024.1.0",
    "identifiers": [
      "picow0_940"
    ]
  }
}
```

bed2 temperature

```javascript
{
  "stat_t": "home/sensor/picow0_940/state",
  "name": "picow0_940-bed2_temp",
  "uniq_id": "picow0_940-abd1-bed2_temp",
  "dev_cla": "temperature",
  "val_tpl": "{{ value_json.bed2_temperature | is_defined }}",
  "unit_of_meas": "F",
  "device": {
    "identifiers": [
      "picow0_940"
    ]
  }
}
```


temperature ambient

```javascript
{
  "stat_t": "home/sensor/picow0_940/state",
  "name": "picow0_940-amb_temp",
  "uniq_id": "picow0_940-bme-amb_temp",
  "dev_cla": "temperature",
  "val_tpl": "{{ value_json.temperature_ambient | is_defined }}",
  "unit_of_meas": "F",
  "device": {
    "identifiers": [
      "picow0_940"
    ]
  }
}
```


humidity ambient

```javascript
{
  "stat_t": "home/sensor/picow0_940/state",
  "name": "picow0_940-amb_humid",
  "uniq_id": "picow0_940-bme-amb_humid",
  "dev_cla": "temperature",
  "val_tpl": "{{ value_json.humidity_ambient | is_defined }}",
  "unit_of_meas": "%",
  "device": {
    "identifiers": [
      "picow0_940"
    ]
  }
}
```




state payload

```json
{
    "bed1_temperature": 68.2,
    "bed2_temperature": 70.9,
    "bed3_temperature": 71.3,
    "humidity_ambient": 35.7,
    "temperature_ambient": 59.3
}
```



#### Discovery topic


 `<discovery_prefix>/<component>/[<node_id>/]<object_id>/config`

 Device (all components at once)
   `homeassistant/device/...`

 Multiple
   `homeassistant/sensor/[]/OID/config`

#### Disocvery payload

https://www.home-assistant.io/integrations/mqtt/#sensors

The shared options at the root level of the JSON message must include:

 - `device` mapping (abbreviated as `dev`)
 - `origin` mapping (abbreviated as `o`)

Examples

Configuration topic no1: homeassistant/sensor/sensorBedroomT/config
Configuration topic no2: homeassistant/sensor/sensorBedroomH/config

state topic (shared):    homeassistant/sensor/sensorBedroom/state

.device.identifiers [ "SHARED" ]

payload no1

```
{
   "device_class":"temperature",
   "state_topic":"homeassistant/sensor/sensorBedroom/state",
   "unit_of_measurement":"°F",
   "value_template":"{{ value_json.temperature_bed1}}",
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


payload no2

```
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




smart button

 - `homeassistant/sensor/0x286d970001037539/temperature/config`

```
{
  "availability": [
    {
      "topic": "zigbee2mqtt/bridge/state",
      "value_template": "{{ value_json.state }}"
    }
  ],
  "device": {
    "hw_version": 0,
    "identifiers": [
      "zigbee2mqtt_0x286d970001037539"
    ],
    "manufacturer": "SmartThings",
    "model": "Button",
    "model_id": "IM6001-BTP01",
    "name": "SmartThings Button 1",
    "sw_version": "",
    "via_device": "zigbee2mqtt_bridge_0x287681fffef04049"
  },
  "device_class": "temperature",
  "enabled_by_default": true,
  "object_id": "smartthings_button_1_temperature",
  "origin": {
    "name": "Zigbee2MQTT",
    "sw": "2.0.0",
    "url": "https://www.zigbee2mqtt.io"
  },
  "state_class": "measurement",
  "state_topic": "zigbee2mqtt/SmartThings Button 1",
  "unique_id": "0x286d970001037539_temperature_zigbee2mqtt",
  "unit_of_measurement": "°C",
  "value_template": "{{ value_json.temperature }}"
}

```

 -  `homeassistant/event/0x286d970001037539/action/config`

```
{
  "availability": [
    {
      "topic": "zigbee2mqtt/bridge/state",
      "value_template": "{{ value_json.state }}"
    }
  ],
  "device": {
    "hw_version": 0,
    "identifiers": [
      "zigbee2mqtt_0x286d970001037539"
    ],
    "manufacturer": "SmartThings",
    "model": "Button",
    "model_id": "IM6001-BTP01",
    "name": "SmartThings Button 1",
    "sw_version": "",
    "via_device": "zigbee2mqtt_bridge_0x287681fffef04049"
  },
  "event_types": [
    "off",
    "single",
    "double",
    "hold"
  ],
  "icon": "mdi:gesture-double-tap",
  "name": "Action",
  "object_id": "smartthings_button_1_action",
  "origin": {
    "name": "Zigbee2MQTT",
    "sw": "2.0.0",
    "url": "https://www.zigbee2mqtt.io"
  },
  "state_topic": "zigbee2mqtt/SmartThings Button 1",
  "unique_id": "0x286d970001037539_action_zigbee2mqtt",
  "value_template": "{% set patterns = [\n{\"pattern\": '^(?P<button>(?:button_)?[a-z0-9]+)_(?P<action>(?:press|hold)(?:_release)?)$', \"groups\": [\"button\", \"action\"]},\n{\"pattern\": '^(?P<action>recall|scene)_(?P<scene>[0-2][0-9]{0,2})$', \"groups\": [\"action\", \"scene\"]},\n{\"pattern\": '^(?P<actionPrefix>region_)(?P<region>[1-9]|10)_(?P<action>enter|leave|occupied|unoccupied)$', \"groups\": [\"actionPrefix\", \"region\", \"action\"]},\n{\"pattern\": '^(?P<action>dial_rotate)_(?P<direction>left|right)_(?P<speed>step|slow|fast)$', \"groups\": [\"action\", \"direction\", \"speed\"]},\n{\"pattern\": '^(?P<action>brightness_step)(?:_(?P<direction>up|down))?$', \"groups\": [\"action\", \"direction\"]}\n] %}\n{% set action_value = value_json.action|default('') %}\n{% set ns = namespace(r=[('action', action_value)]) %}\n{% for p in patterns %}\n  {% set m = action_value|regex_findall(p.pattern) %}\n  {% if m[0] is undefined %}{% continue %}{% endif %}\n  {% for key, value in zip(p.groups, m[0]) %}\n    {% set ns.r = ns.r|rejectattr(0, 'eq', key)|list + [(key, value)] %}\n  {% endfor %}\n{% endfor %}\n{% if (ns.r|selectattr(0, 'eq', 'actionPrefix')|first) is defined %}\n  {% set ns.r = ns.r|rejectattr(0, 'eq', 'action')|list + [('action', ns.r|selectattr(0, 'eq', 'actionPrefix')|map(attribute=1)|first + ns.r|selectattr(0, 'eq', 'action')|map(attribute=1)|first)] %}\n{% endif %}\n{% set ns.r = ns.r + [('event_type', ns.r|selectattr(0, 'eq', 'action')|map(attribute=1)|first)] %}\n{{dict.from_keys(ns.r|rejectattr(0, 'in', ('action', 'actionPrefix'))|reject('eq', ('event_type', None))|reject('eq', ('event_type', '')))|to_json}}"
}
```

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


Setting up a sensor with multiple measurement values requires multiple consecutive configuration topic submissions.

The sensor identifiers or connections option allows to set up multiple entities that share the same device.

If a device configuration is shared, then it is not needed to add all device details to the other entity configs. It is enough to add shared identifiers or connections to the device mapping for the other entity config payloads.

A common state payload that can be parsed with the value_template in the sensor configs:




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


## MQTT explorer


`homeassistant/sensor/0x286d970001037539/temperature/config`

```json
{
  "availability": [
    {
      "topic": "zigbee2mqtt/bridge/state",
      "value_template": "{{ value_json.state }}"
    }
  ],
  "device": {
    "hw_version": 0,
    "identifiers": [
      "zigbee2mqtt_0x286d970001037539"
    ],
    "manufacturer": "SmartThings",
    "model": "Button",
    "model_id": "IM6001-BTP01",
    "name": "SmartThings Button 1",
    "sw_version": "",
    "via_device": "zigbee2mqtt_bridge_0x287681fffef04049"
  },
  "device_class": "temperature",
  "enabled_by_default": true,
  "object_id": "smartthings_button_1_temperature",
  "origin": {
    "name": "Zigbee2MQTT",
    "sw": "2.0.0",
    "url": "https://www.zigbee2mqtt.io"
  },
  "state_class": "measurement",
  "state_topic": "zigbee2mqtt/SmartThings Button 1",
  "unique_id": "0x286d970001037539_temperature_zigbee2mqtt",
  "unit_of_measurement": "°C",
  "value_template": "{{ value_json.temperature }}"
}

```

## non-micropython

<https://github.com/unixorn/ha-mqtt-discoverable#sensor>


homeassistant/sensor/A4C138C38EE5-LYWSD03MMC-batt/config
```
{
  "stat_t": "home/OpenMQTTGateway_ESP32_BLE/BTtoMQTT/A4C138C38EE5",
  "name": "LYWSD03MMC-batt",
  "uniq_id": "A4C138C38EE5-LYWSD03MMC-batt",
  "dev_cla": "battery",
  "val_tpl": "{{ value_json.batt | is_defined }}",
  "unit_of_meas": "%",
  "device": {
    "name": "A4C138C38EE5",
    "model": "LYWSD03MMC",
    "manufacturer": "OMG_community",
    "identifiers": [
      "A4C138C38EE5"
    ]
  }
}
```
homeassistant/sensor/A4C138C38EE5-LYWSD03MMC-volt/config
```
{
  "stat_t": "home/OpenMQTTGateway_ESP32_BLE/BTtoMQTT/A4C138C38EE5",
  "name": "LYWSD03MMC-volt",
  "uniq_id": "A4C138C38EE5-LYWSD03MMC-volt",
  "val_tpl": "{{ value_json.volt | is_defined }}",
  "unit_of_meas": "V",
  "device": {
    "name": "A4C138C38EE5",
    "model": "LYWSD03MMC",
    "manufacturer": "OMG_community",
    "identifiers": [
      "A4C138C38EE5"
    ]
  }
}
```
homeassistant/sensor/A4C138C38EE5-LYWSD03MMC-tempc/config
```
{
  "stat_t": "home/OpenMQTTGateway_ESP32_BLE/BTtoMQTT/A4C138C38EE5",
  "name": "LYWSD03MMC-tempc",
  "uniq_id": "A4C138C38EE5-LYWSD03MMC-tempc",
  "dev_cla": "temperature",
  "val_tpl": "{{ value_json.tempc | is_defined }}",
  "unit_of_meas": "Â°C",
  "device": {
    "name": "A4C138C38EE5",
    "model": "LYWSD03MMC",
    "manufacturer": "OMG_community",
    "identifiers": [
      "A4C138C38EE5"
    ]
  }
}
```

homeassistant/sensor/A4C138C38EE5-LYWSD03MMC-hum/config
```
{
  "stat_t": "home/OpenMQTTGateway_ESP32_BLE/BTtoMQTT/A4C138C38EE5",
  "name": "LYWSD03MMC-hum",
  "uniq_id": "A4C138C38EE5-LYWSD03MMC-hum",
  "dev_cla": "humidity",
  "val_tpl": "{{ value_json.hum | is_defined }}",
  "unit_of_meas": "%",
  "device": {
    "name": "A4C138C38EE5",
    "model": "LYWSD03MMC",
    "manufacturer": "OMG_community",
    "identifiers": [
      "A4C138C38EE5"
    ]
  }
}
```

For this message :
```
{
  "id": "A4:C1:38:C3:8E:E5",
  "name": "ATC_C38EE5",
  "rssi": -73,
  "model": "LYWSD03MMC_ATC",
  "tempc": 24.3,
  "tempf": 75.74,
  "hum": 50,
  "batt": 49,
  "volt": 2.522
}
```
