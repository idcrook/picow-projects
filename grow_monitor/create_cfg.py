#!/usr/bin/env python3

import json

example_config = {
    "i2c": {
        "bme280_address": 0x77,
        "ssd1306_address": 0x3c,
        "ssd1306_width": 128,
        "ssd1306_height": 32,
        "sda_pin": 4,
        "scl_pin": 5
    },
    "onewire": {
        "data_pin": 26
    },
    "wifi": {
        "ssid": "guest_net",
        "password": "mypassword"
    },
    "global": {
        "sensor_read_interval_seconds": 30,
        "enable_bme": False
     },
    "mqtt": {
        "broker": "192.168.1.2",
        "port": 1883,
        "topic_root": "picow0"
    }
}


# write json file
output_json = 'config.example.json'
with open(output_json, 'w') as jsonfile:
    print('saving to', output_json)
    json.dump(example_config, jsonfile, indent=2)
