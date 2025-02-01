# per-device numbers and names

ONEWIRE_CONFIG = {
    "data_pin": 22,
    "sensors": {
        "288f8746b1220767": {"name": "bed1"},
        "28ffdb8483160410": {"name": "bed3"},
        "288d85b8b022061b": {"name": "bed4"},
        "2834e359b1220734": {"name": "bed2"},
    },
}

I2C_CONFIG = {
    "bus": {
        "bus_number": 0,
        "sda_pin": 4,
        "scl_pin": 5
    },
    "sensors" : [
        { "bme280":
          { "address": 119,
           }
         }
    ],
    "displays" : [
        { "ssd1306" :
          {
              "address": 60,
              "width": 128,
              "height": 32,
          }
         }
    ]
}


APP_CONFIG = {
    "sensor_read_interval_seconds": 30,
    "device_name": "picow0",
    # "unique_id"
}
