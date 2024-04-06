import binascii
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
DEFAULT_ONEWIRE_SENSOR_ID = "1"
DEFAULT_ONEWIRE_TOPIC = "bed"
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
onewire_sensors = ONEWIRE_CONF.get('sensors', {})

# Populate topics
DS_TOPICS = {}
for sensor_data in onewire_sensors:
    for sensor_id in sensor_data:
        topic = sensor_data[sensor_id]['topic']
        # print(sensor_id, topic)
        DS_TOPICS[sensor_id] = topic
if not bool(DS_TOPICS):
    DS_TOPICS[DEFAULT_ONEWIRE_SENSOR_ID] = DEFAULT_ONEWIRE_TOPIC

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
ds_roms_lookup = {}
print("Configured sensors:", DS_TOPICS)
if len(ds_roms) > 0:
    ONEWIRE_ENABLED = True
    auto_populate_topics = False
    i = 1
    if DS_TOPICS.pop(DEFAULT_ONEWIRE_SENSOR_ID, False):
        auto_populate_topics = True
        print("Will auto-populate topics")
    for device in ds_roms:
        s = binascii.hexlify(device)
        readable_string = s.decode('ascii')
        print(readable_string, ds_sensor.read_temp(device))
        ds_roms_lookup[readable_string] = device
        if auto_populate_topics:
            DS_TOPICS[readable_string] = DEFAULT_ONEWIRE_TOPIC + str(i)
            i = i + 1
            print(readable_string, DS_TOPICS[readable_string])
else:
    print("No DS sensors found.")


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
    display.text('ip addr:', 0, 0, 0)
    display.text('' + status[0], 0, 23, 0)
    display.show()
    await asyncio.sleep(2)

    PROBE_TEMPERATURES = {}
    probe_temperature = str(round(0.0, 1)) + 'F'
    read_count = 0
    publish_count_debug_show_each = 10

    for rom_readable in ds_roms_lookup:
        PROBE_TEMPERATURES[rom_readable] = probe_temperature

    # Main sensor read loop
    while True:

        if ONEWIRE_ENABLED:
            # trigger sensor read
            ds_sensor.convert_temp()
            await asyncio.sleep_ms(750)

            # for rom in ds_roms:
            #     probe_temperature = getDSTemperature(ds_sensor, rom)
            #     print(probe_temperature, end=' ')

            for rom_readable in ds_roms_lookup:
                rom = ds_roms_lookup[rom_readable]
                probe_temperature = getDSTemperature(ds_sensor, rom)
                print('..' + rom_readable[-2:], probe_temperature, end=' ')
                PROBE_TEMPERATURES[rom_readable] = probe_temperature

            read_count += 1

        # publish temperatures
        for rom_readable in ds_roms_lookup:
            probe_temperature = PROBE_TEMPERATURES[rom_readable]
            probe_topic = MQTT_TOPIC_ROOT + '/' + DS_TOPICS[rom_readable] + '/probe'
            probe_obj = {'temperature': probe_temperature}
            # print(probe_topic, probe_temperature)
            await client.publish(probe_topic,
                                 json.dumps(probe_obj), qos=1)

        # publish status
        topic = MQTT_TOPIC_ROOT + '/status'
        status_obj = {'sensor_reads': read_count}
        await client.publish(topic,
                             json.dumps(status_obj), qos=1)


        if (read_count % publish_count_debug_show_each == 0):
            print('')
            print("Sensor reads so far:", str(status_obj))

        if ONEWIRE_ENABLED:
            # show on display
            display.fill(0)
            display.text("R:" + str(read_count), 0, 1, 1)
            y = starting_y = 16
            offset = 12
            for probe in PROBE_TEMPERATURES:
                temperature_str = PROBE_TEMPERATURES[probe]
                display.text(DS_TOPICS[probe] + ' ' + temperature_str,
                             0, y, 1)
                y = y + offset
            display.show()

        await asyncio.sleep(SENSOR_READ_INTERVAL)

config["queue_len"] = 1  # Use event interface with default queue size
# MQTTClient.DEBUG = True  # Optional: print diagnostic messages
Client = MQTTClient(config)
try:
    asyncio.run(main(Client))
finally:
    Client.close()  # Prevent LmacRxBlk:1 errors
