# micropython program to publish sensor data to MQTT for use by Home Assistant
#
# See TODO.md

# import errno
import time
import network
import binascii
import json
import sys
from collections import OrderedDict

import asyncio
import ds18x20
import onewire
from onewire import OneWireError
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C

# Third party libraries
sys.path.append("/third-party")
from mqtt_as import MQTTClient
from mqtt_as import config as mqtt_config
from micropython_bmpxxx import bmpxxx

import config
from config import ONEWIRE_CONFIG, I2C_CONFIG, APP_CONFIG
from config import unique_device_identifier, set_mqtt_disc_dev_id, CFG_DEV
from secrets import WIFI_SSID, WIFI_PASSWORD, MQTT_SERVER #, MQTT_PORT, MQTT_USER, MQTT_PASSWORD

ssid = WIFI_SSID
password = WIFI_PASSWORD
DEVNAME = APP_CONFIG.setdefault("device_name", "picow999")

# https://docs.micropython.org/en/latest/library/network.html#network.hostname
network.hostname(DEVNAME)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

mac = binascii.hexlify(network.WLAN().config('mac'),':').decode()
udi = unique_device_identifier(mac)

# use name and unique device ID to generate if not specified
UNIQ_ID_PRE = APP_CONFIG.setdefault("unique_id", f"{DEVNAME}_{udi}")
print(DEVNAME, mac, udi, UNIQ_ID_PRE)
set_mqtt_disc_dev_id(UNIQ_ID_PRE)
print(CFG_DEV)

########################################################################
#  Detect devices from the config files
SENSOR_STATES_TO_USE = {
    "bed1_temperature": None,
    "bed2_temperature": None,
    "bed3_temperature": None,
    "humidity_ambient": None,
    "temperature_ambient": None
}

def _get_ds_state_name(name):
    return  f"{name}_temperature"

########################################################################
# 1-wire configs
ds_pin = Pin(ONEWIRE_CONFIG.get("data_pin", 22))
DS_SENSOR_IFC = ds18x20.DS18X20(onewire.OneWire(ds_pin))

DS_SENSORS = ONEWIRE_CONFIG.get("sensors", {})
DS_SENSORS_FOUND = {}


roms = DS_SENSOR_IFC.scan()
for device in roms:
    s = binascii.hexlify(device)
    readable = s.decode('ascii')
    #print(readable)
    if readable in DS_SENSORS:
        info = {}
        info['name'] = DS_SENSORS[readable]['name']
        info['object_id'] = readable[-4:]
        info['device_type'] = 'ds18b20'
        info['interface'] = device
        DS_SENSORS_FOUND[readable] = info
        state_to_use = _get_ds_state_name(info['name'])
        SENSOR_STATES_TO_USE[state_to_use] = info['object_id']

print ("found 1-wire(s)", DS_SENSORS_FOUND)

if True:
    DS_SENSOR_IFC.convert_temp()
    time.sleep_ms(750)

    try:
        for s_id, s_params in DS_SENSORS_FOUND.items():
            device = s_params['interface']
            temperature = round(DS_SENSOR_IFC.read_temp(device), 1)
            print(s_id, temperature, "C")
    except OneWireError as error:
        print("error with", device)
        print(error)
        # FIXME: hopefully a transient issue but add better handling
        pass

########################################################################
# I2C configs
i2c_bus_info = I2C_CONFIG['bus']
i2c_bus = i2c_bus_info['bus_number']
i2c_sda = Pin(i2c_bus_info['sda_pin'])
i2c_scl = Pin(i2c_bus_info['scl_pin'])

i2c = I2C(i2c_bus, sda=i2c_sda, scl=i2c_scl)

# I2C sensors config - bme280
I2C_SENSORS = I2C_CONFIG.get('sensors', [])
I2C_SENSORS_FOUND = {}

for sensor in I2C_SENSORS:
    for s_type, s_params in sensor.items():
        if s_type == 'bme280':
            address = s_params.setdefault('address', 0x77)
            # FIXME: Handle RuntimeError if not found, e.g.
            # RuntimeError: BME280 sensor not found at specified I2C address (0x77).
            this = bmpxxx.BME280(i2c, address=address)
            info = {}
            info['device_type'] = s_type
            info['address'] = address
            info['object_id'] = 'amb'
            info['interface'] = this
            I2C_SENSORS_FOUND[address] = info
            sensor_to_use = 'temperature_ambient'
            SENSOR_STATES_TO_USE[sensor_to_use] = "ambT"
            sensor_to_use = 'humidity_ambient'
            SENSOR_STATES_TO_USE[sensor_to_use] = "ambH"


for i2c_address, s_params in I2C_SENSORS_FOUND.items():
    sensor_interface = s_params['interface']
    name = s_params['device_type']
    if name == 'bme280':
        temperature = sensor_interface.temperature
        humidity = sensor_interface.humidity
        dewpoint = sensor_interface.dew_point
        print(f"{name}:> {temperature:.1f}C rel humid:{humidity:.1f}% dewpt:{dewpoint:.1f}C")

########################################################################
# I2C displays config
I2C_DISPLAYS = []
I2C_DISPLAYS_FOUND = False
i2c_displays = I2C_CONFIG.get('displays', [])

I2C_USE_DISPLAYS = APP_CONFIG.get('display_temperature_readings', False)

# assume zero or one (no more) display for now
if len(i2c_displays) and I2C_USE_DISPLAYS:
    display_info = i2c_displays[0]
    #print(display_info)
    for d_type, d_params in display_info.items():
        address = d_params['address']
        h = d_params['height']
        w = d_params['width']
        display = SSD1306_I2C(w, h, i2c)
        display.fill(0)
        display.text(DEVNAME, 0, 0, 1)
        display.text(UNIQ_ID_PRE, 0, 12, 1)
        display.show()
        info = {'device_type': d_type, 'interface': display,
                'height': h, 'width': w}
        info.update(d_params)
        I2C_DISPLAYS_FOUND = True
        I2C_DISPLAYS.append(info)

print("displays found:", I2C_DISPLAYS)
if I2C_DISPLAYS_FOUND:
    time.sleep(2)
    I2C_DISPLAYS[0]['interface'].fill(0)
    I2C_DISPLAYS[0]['interface'].show()


def _display_readings(values):
    print(values)
    display = I2C_DISPLAYS[0]['interface']
    width = I2C_DISPLAYS[0]['width']
    height = I2C_DISPLAYS[0]['height'] # use for height check?

    line_height = 12
    total_columns = 2
    reading_width = width // total_columns

    display.fill(0)
    line_no = 0
    column_no = 0
    for short_name, value in values.items():
        if short_name.startswith('bed'):
            s = f"{short_name[-2:]} {value:.1f}F"
        else:
            s = f"{short_name}{value}"
            if  short_name.startswith('amb') and column_no != 0:
                # start new line
                line_no = line_no + 1
                column_no = 0

        x = column_no * reading_width
        y = line_no * line_height
        print(y, x, s)
        display.text(s, x, y, 1)
        (line_no, column_no) = divmod (line_no * total_columns + column_no + 1,
                                       total_columns)
    display.show()

########################################################################


print(SENSOR_STATES_TO_USE)

def cvt_CtoF(temperature):
    return round((9. / 5.) * temperature + 32.0, 1)

async def messages(client):  # Respond to incoming messages
    # If MQTT V5is used this would read
    # async for topic, msg, retained, properties in client.queue:
    async for topic, msg, retained in client.queue:
        print(topic.decode(), msg.decode(), retained)

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        # await client.subscribe('foo_topic', 1)  # renew subscriptions

async def main(client):
    # Wi-Fi network starts here, using mqtt_as capability
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))

    state_topic = await mqtt_discovery(client)

    n = 0
    display_values = OrderedDict([])
    while True:
        n = n + 1
        state_update = {}
        display_values['N'] = f"={n:>5,}"

        DS_SENSOR_IFC.convert_temp()
        time.sleep_ms(750)

        try:
            for s_id, s_params in DS_SENSORS_FOUND.items():
                device = s_params['interface']
                name = s_params['name']
                state_name = _get_ds_state_name(name)
                temperature = round(DS_SENSOR_IFC.read_temp(device), 1)
                # print(s_id, name, temperature, "C")
                tF = cvt_CtoF(temperature)
                state_update[state_name] = tF
                display_values[name] = tF
        except OneWireError as error:
            print("error with", device)
            print(error)
            # FIXME: hopefully a transient issue but add better handling
            pass

        for i2c_address, s_params in I2C_SENSORS_FOUND.items():
            sensor_interface = s_params['interface']
            name = s_params['device_type']
            if name == 'bme280':
                temperature = round(sensor_interface.temperature, 1)
                humidity = round(sensor_interface.humidity, 1)
                # print(f"{name}:> {temperature:.1f}C rel humid:{humidity:.1f}% dewpt:{dewpoint:.1f}C")
                tF = cvt_CtoF(temperature)
                state_update['temperature_ambient'] = tF
                state_update['humidity_ambient'] = humidity
                display_value = f" {tF:.1f}F {humidity:.0f}%"
                display_values['amb'] = display_value


        pub_payload = json.dumps(state_update)
        # print(state_topic, pub_payload)
        await client.publish(state_topic, bytes(pub_payload, 'utf-8'), qos=1)
        if I2C_DISPLAYS_FOUND:
            _display_readings(display_values)
        await asyncio.sleep(APP_CONFIG.get('sensor_read_interval_seconds', 30))


async def mqtt_discovery(client):

    state_topic = TOP_TOPIC + f"/sensor/{UNIQ_ID_PRE}/state"

    first_ds = True
    for s_id, s_params in DS_SENSORS_FOUND.items():
        readable = s_params['object_id']
        name =  s_params['name']
        state_name = _get_ds_state_name(name)
        topic = TOP_TOPIC + f"/sensor/{UNIQ_ID_PRE}/{readable}/config"
        payload = {
            "name": f"{name}_temp",
            # "state_class": "measurement",
            "device_class": "temperature",
            "state_topic": state_topic,
            "unit_of_measurement": "°F",
            "value_template": f"{{{{ value_json.{state_name} | is_defined }}}}",
            "unique_id": f"{UNIQ_ID_PRE}_{readable}_{name}_temp",
            "device" : CFG_DEV,
        }
        if first_ds:
            first_ds = False
        else:
            payload['device'] = {}
            payload['device']['ids'] = CFG_DEV['ids']

        message = json.dumps(payload)
        #print(topic, message)
        await client.publish(topic, bytes(message, 'utf-8'), qos=1)

    for i2c_address, s_params in I2C_SENSORS_FOUND.items():
        name = s_params['device_type']
        address = s_params['address']
        valueT = 'temperature_ambient'
        topicT = TOP_TOPIC + f"/sensor/{UNIQ_ID_PRE}/ambT/config"
        payloadT = {
            "stat_t": state_topic,
            "name": "amb_temp",
            "uniq_id": f"{UNIQ_ID_PRE}_{name}_{address}_amb_temp",
            "dev_cla": "temperature",
            "val_tpl": f"{{{{ value_json.{valueT} | is_defined }}}}",
            "unit_of_meas": "°F",
            "device" : {  "ids":  CFG_DEV['ids']  },
        }
        messageT = json.dumps(payloadT)
        #print(topicT, messageT)
        await client.publish(topicT, bytes(messageT, 'utf-8'), qos=1)

        valueH = 'humidity_ambient'
        topicH = TOP_TOPIC + f"/sensor/{UNIQ_ID_PRE}/ambH/config"
        payloadH = {
            "stat_t": state_topic,
            "name": "amb_humid",
            "uniq_id": f"{UNIQ_ID_PRE}_{name}_{address}_amb_humid",
            "dev_cla": "humidity",
            "val_tpl": f"{{{{ value_json.{valueH} | is_defined }}}}",
            "unit_of_meas": "%",
            "device" : {  "ids":  CFG_DEV['ids']  },
        }
        messageH = json.dumps(payloadH)
        #print(topicH, messageH)
        await client.publish(topicH, bytes(messageH, 'utf-8'), qos=1)


    return state_topic

TOP_TOPIC = config.get_top_topic()

mqtt_config['ssid'] = WIFI_SSID
mqtt_config['wifi_pw'] = WIFI_PASSWORD
mqtt_config['server'] = MQTT_SERVER
mqtt_config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(mqtt_config)

# on macOS: brew install mosquitto
print(f"mosquitto_sub -h {MQTT_SERVER} -t {TOP_TOPIC}/sensor/{UNIQ_ID_PRE}/\\#")


try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
