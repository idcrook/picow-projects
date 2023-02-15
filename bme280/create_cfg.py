#!/usr/bin/env python3

import json

example_config = { 
  "i2c" :
        { "bme280_address" : 0x77,
          "ssd1306_address" : 0x3c,
          "ssd1306_width" : 128,
          "ssd1306_height" : 32,
          "sda_pin" : 4,
          "scl_pin": 5
        }, 
  "wifi" :
        { "ssid" : "guest_net",
           "password": "mypassword"
        },
  "mqtt":
        { 
          "broker" : "192.168.1.2",
          "port" : 1883,
          "topic_root" : "picow0"
        }
}


# write json file
output_json = 'config.example.json'
with open(output_json, 'w') as jsonfile:
    print('saving to', output_json)
    json.dump(example_config, jsonfile, indent=2)
