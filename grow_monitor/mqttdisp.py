from machine import Pin, I2C
import network
import os, sys, errno
from time import sleep, sleep_ms
import bme280
from umqtt.simple import MQTTClient
from ssd1306 import SSD1306_I2C
import onewire, ds18x20
import json

# subscribe to topic picow0/# on http://192.168.50.6:9001/

config_file = 'config.secrets.json'
ONEWIRE_ENABLED = False

DEFAULT_SDA_PIN = 17
DEFAULT_SCL_PIN = 16
DEFAULT_I2C_BME280_ADDRESS = 0x76
DEFAULT_I2C_SSD1306_ADDRESS = 0x3c
DEFAULT_I2C_SSD1306_WIDTH = 128
DEFAULT_I2C_SSD1306_HEIGHT = 64
DEFAULT_ONEWIRE_DATA_PIN = 26
DEFAULT_WIFI_SSID = "Guest"
DEFAULT_WIFI_PASSWORD = "password"
DEFAULT_MQTT_BROKER=b"192.168.1.6"
DEFAULT_MQTT_PORT=1883
DEFAULT_MQTT_TOPIC_ROOT="picow0"
DEFAULT_SENSOR_READ_INTERVAL_SECONDS = 15

CONFIG = {}

try:
    with open(config_file, 'r') as jsonfile:
        CONFIG = json.loads(jsonfile.read())
        print (CONFIG)
except OSError as ose:
    if ose.errno not in (errno.ENOENT,):
        # this re-raises the same error object.
        raise
    pass # ENOENT. 

# subtrees of the config file
MQTT_CONF = CONFIG.get("mqtt", {})  
I2C_CONF = CONFIG.get("i2c", {})
WIFI_CONF = CONFIG.get("wifi", {})
ONEWIRE_CONF = CONFIG.get("onewire", {})
GLOBAL_CONF = CONFIG.get("global", {})

sensor_read_interval = GLOBAL_CONF.get('sensor_read_interval_seconds', DEFAULT_SENSOR_READ_INTERVAL_SECONDS)

sda_pin = I2C_CONF.get('sda_pin', DEFAULT_SDA_PIN)  # assume default here if not found
scl_pin = I2C_CONF.get('scl_pin', DEFAULT_SCL_PIN)

i2c_bme280_addr =  I2C_CONF.get('bme280_address', DEFAULT_I2C_BME280_ADDRESS)
i2c_ssd1306_addr =  I2C_CONF.get('ssd1306_address', DEFAULT_I2C_SSD1306_ADDRESS)
i2c_ssd1306_width =  I2C_CONF.get('ssd1306_width', DEFAULT_I2C_SSD1306_WIDTH)
i2c_ssd1306_height =  I2C_CONF.get('ssd1306_height', DEFAULT_I2C_SSD1306_HEIGHT)

# initialize display so can display network status
try:
    i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
except ValueError as ve:
    print("ERROR: Cannot connect to I2C bus for pins sda={}, scl={}".format(sda_pin, scl_pin))
    print("Check settings in file", config_file, "on device")
    raise

bme = bme280.BME280(i2c=i2c, address=i2c_bme280_addr)
display = SSD1306_I2C(i2c_ssd1306_width, i2c_ssd1306_height, i2c, 
                      addr=i2c_ssd1306_addr)

wifi_ssid = WIFI_CONF.get('ssid', DEFAULT_WIFI_SSID)
wifi_password = WIFI_CONF.get('password', DEFAULT_WIFI_PASSWORD)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)

display.fill(0)
display.text("Waiting on WiFi", 3, 0, 1)
display.show()

# Wait for connect or fail
max_wait = 10
dot_position = 0
dot_incr = 6

while max_wait > 0:

    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection')
    display.text(".", 3 + dot_position, 11, 1)
    display.show()
    dot_position = dot_position + dot_incr
    sleep(2)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')

status = wlan.ifconfig()
print('ip = ' + status[0])
display.fill(0)
display.text('ip addr:', 0, 11, 1)
display.text('' + status[0], 0, 23, 1)
display.show()

# Initialize onewire devices
onewire_data_pin = ONEWIRE_CONF.get('data_pin', DEFAULT_ONEWIRE_DATA_PIN) 
ds_sensor = ds18x20.DS18X20(onewire.OneWire(Pin(onewire_data_pin)))
ds_roms = ds_sensor.scan()
if len(ds_roms) > 0:
    ONEWIRE_ENABLED = True

MQTT_BROKER = bytes(MQTT_CONF.get('broker', DEFAULT_MQTT_BROKER), 'utf-8')
MQTT_PORT = MQTT_CONF.get('port', DEFAULT_MQTT_PORT)
MQTT_TOPIC_ROOT = MQTT_CONF.get('topic_root', DEFAULT_MQTT_PORT)

def connectMQTT():
    client = MQTTClient(client_id=b"picow0_grow_monitor",
                        server=MQTT_BROKER,
                        port=MQTT_PORT,
                        #user=b"mydemoclient",
                        #password=b"passowrd",
                        keepalive=7200,
                        # ssl=False, #ssl=True,
                        )
    client.connect()
    return client


# connect to MQTT broker
client = connectMQTT()

def publish(topic, value):
    # print(topic, value)
    client.publish(topic, value)
    # print("publish Done",)

def conv_CtoF(temperature):
    return (9./5.)*temperature + 32.0

def getDSTemperature(ds, rom):
    tempC = ds.read_temp(rom)
    temp = str(round(conv_CtoF(tempC),1)) + 'F'
    return temp

probe_temperature = str(round(0.0, 1)) + 'F'

while True:
    sensor_reading = bme
    temperature = sensor_reading.values[0]
    pressure = sensor_reading.values[1]
    humidity = sensor_reading.values[2]

    print(sensor_reading.values)

    if ONEWIRE_ENABLED:
        # trigger sensor read
        ds_sensor.convert_temp()
        sleep_ms(750)

        for rom in ds_roms:
            probe_temperature = getDSTemperature(ds_sensor, rom)
            print(probe_temperature)

        # publish as MQTT payload
        publish(MQTT_TOPIC_ROOT + '/probe_temperature', probe_temperature)

    publish(MQTT_TOPIC_ROOT + '/temperature', temperature)
    publish(MQTT_TOPIC_ROOT + '/humidity', humidity)
    publish(MQTT_TOPIC_ROOT + '/pressure', pressure)

    # show on display
    display.fill(0)
    if ONEWIRE_ENABLED:
        display.text("Tmp " + bme.values[0] + " " + probe_temperature, 3, 0, 1)
    else:
        display.text("Temp " + bme.values[0], 3, 0, 1)

    display.text("PA  " + bme.values[1], 3, 11, 1)
    display.text("Humidity " + bme.values[2], 3, 23, 1)
    display.show()

    # delay for number of seconds
    sleep(sensor_read_interval)
