import errno
from machine import Pin, I2C
from time import sleep, sleep_ms
import asyncio
from ssd1306 import SSD1306_I2C
import onewire
import ds18x20
import json
from mqtt_as import MQTTClient, config

# subscribe to topic picow0/# on http://192.168.50.6:9001/

CONFIG_FILE = 'config.secrets.json'
ONEWIRE_ENABLED = False

DEFAULT_SDA_PIN = 17
DEFAULT_SCL_PIN = 16
DEFAULT_I2C_SSD1306_ADDRESS = 0x3c
DEFAULT_I2C_SSD1306_WIDTH = 128
DEFAULT_I2C_SSD1306_HEIGHT = 64
DEFAULT_ONEWIRE_DATA_PIN = 26
DEFAULT_WIFI_SSID = "Guest"
DEFAULT_WIFI_PASSWORD = "password"
DEFAULT_MQTT_BROKER = b"192.168.1.6"
DEFAULT_MQTT_PORT = 1883
DEFAULT_MQTT_TOPIC_ROOT = "picow0"
DEFAULT_SENSOR_READ_INTERVAL_SECONDS = 15

CONFIG = {}

try:
    with open(CONFIG_FILE, 'r') as jsonfile:
        CONFIG = json.loads(jsonfile.read())
        print(CONFIG)
except OSError as ose:
    if ose.errno not in (errno.ENOENT,):
        # this re-raises the same error object.
        raise

# subtrees of the config file
MQTT_CONF = CONFIG.get("mqtt", {})
I2C_CONF = CONFIG.get("i2c", {})
WIFI_CONF = CONFIG.get("wifi", {})
ONEWIRE_CONF = CONFIG.get("onewire", {})
GLOBAL_CONF = CONFIG.get("global", {})

SENSOR_READ_INTERVAL = GLOBAL_CONF.get('sensor_read_interval_seconds',
                                       DEFAULT_SENSOR_READ_INTERVAL_SECONDS)

# Assume defaults if not found in config
sda_pin = I2C_CONF.get('sda_pin', DEFAULT_SDA_PIN)
scl_pin = I2C_CONF.get('scl_pin', DEFAULT_SCL_PIN)

i2c_ssd1306_addr = I2C_CONF.get('ssd1306_address', DEFAULT_I2C_SSD1306_ADDRESS)
i2c_ssd1306_width = I2C_CONF.get('ssd1306_width', DEFAULT_I2C_SSD1306_WIDTH)
i2c_ssd1306_height = I2C_CONF.get('ssd1306_height', DEFAULT_I2C_SSD1306_HEIGHT)

onewire_data_pin = ONEWIRE_CONF.get('data_pin', DEFAULT_ONEWIRE_DATA_PIN)

wifi_ssid = WIFI_CONF.get('ssid', DEFAULT_WIFI_SSID)
wifi_password = WIFI_CONF.get('password', DEFAULT_WIFI_PASSWORD)
config['ssid'] = wifi_ssid
config['wifi_pw'] = wifi_password

MQTT_BROKER = bytes(MQTT_CONF.get('broker', DEFAULT_MQTT_BROKER), 'utf-8')
MQTT_PORT = MQTT_CONF.get('port', DEFAULT_MQTT_PORT)
MQTT_TOPIC_ROOT = MQTT_CONF.get('topic_root', DEFAULT_MQTT_PORT)
config['server'] = MQTT_BROKER

# Initialize display early so can display network status
try:
    i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
except ValueError as ve:
    print("ERROR: Cannot connect to I2C bus for pins sda={}, scl={}".format(
        sda_pin, scl_pin))
    print("Check settings in file", CONFIG_FILE, "on device")
    raise

display = SSD1306_I2C(i2c_ssd1306_width, i2c_ssd1306_height, i2c,
                      addr=i2c_ssd1306_addr)

# show on display
display.fill(0)
# draw some text at x=0, y=0, colour=1
display.text("Starting up...", 0, 0, 1)
display.show()

# Initialize onewire device(s)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(Pin(onewire_data_pin)))
ds_roms = ds_sensor.scan()
if len(ds_roms) > 0:
    ONEWIRE_ENABLED = True


def conv_CtoF(temperature):
    return (9./5.)*temperature + 32.0


def getDSTemperature(ds, rom):
    """ Get DS temperature reading. Return string in Fahrenheit."""
    tC = ds.read_temp(rom)
    temperatureInFstr = str(round(conv_CtoF(tC), 1)) + 'F'
    return temperatureInFstr


# Not currently used
async def messages(client):
    """ Respond to incoming messages. """
    async for topic, msg, retained in client.queue:
        print((topic, msg, retained))


async def up(client):
    """ Respond to connectivity being (re)established. """
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        # await client.subscribe('foo_topic', 1)  # renew subscriptions


async def main(client):
    print('Connect...')
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))

    # Access internal client details to get some network status
    status = client._sta_if.ifconfig()
    print('ip = ' + status[0])
    display.fill(1)
    display.text('ip addr:', 0, 11, 0)
    display.text('' + status[0], 0, 23, 0)
    display.show()
    await asyncio.sleep(2)

    probe_temperature = str(round(0.0, 1)) + 'F'
    read_count = 0
    publish_count_debug_show_each = 10

    # Main sensor read loop
    while True:

        if ONEWIRE_ENABLED:
            # trigger sensor read
            ds_sensor.convert_temp()
            await asyncio.sleep_ms(750)

            for rom in ds_roms:
                probe_temperature = getDSTemperature(ds_sensor, rom)
                print(probe_temperature, end=' ')

            read_count += 1

        # publish as MQTT payload
        status_obj = {'sensor_reads': read_count,
                      'probe_temperature': probe_temperature}
        # await client.publish(MQTT_TOPIC_ROOT + '/probe_temperature',
        #                      probe_temperature, qos=1)
        await client.publish(MQTT_TOPIC_ROOT + '/status',
                             json.dumps(status_obj), qos=1)
        if (read_count % publish_count_debug_show_each == 0):
            print('')
            print("Sensor reads so far:", str(status_obj))

        if ONEWIRE_ENABLED:
            # show on display
            display.fill(0)
            display.text(probe_temperature + " " + "R:" + str(read_count),
                         3, 0, 1)
            display.show()

        await asyncio.sleep(SENSOR_READ_INTERVAL)

config["queue_len"] = 1  # Use event interface with default queue size
# MQTTClient.DEBUG = True  # Optional: print diagnostic messages
Client = MQTTClient(config)
try:
    asyncio.run(main(Client))
finally:
    Client.close()  # Prevent LmacRxBlk:1 errors
