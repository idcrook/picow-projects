# per-device numbers and names

ONEWIRE_CONFIG = {
    "data_pin": 26,
    "sensors": [
      {
        "288f8746b1220767": {
          "topic": "bed1"
        }
      },
      {
        "28ffdb8483160410": {
          "topic": "bed3"
        }
      },
      {
        "2834e359b1220734": {
          "topic": "bed2"
        }
      }
    ]
}

I2C_CONFIG = {
    "bus": {
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
              "height": 64,
          }
         }
    ]
}


APP_CONFIG = {
    "sensor_read_interval_seconds": 30,
    "device_name": "picow0"
}
