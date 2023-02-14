from machine import Pin, I2C
import network
from time import sleep
import bme280
from umqtt.simple import MQTTClient
from ssd1306 import SSD1306_I2C

# subscribe to topic picow0/# on http://192.168.50.6:9001/

I2C_BME280_ADDRESS = 0x77
I2C_SSD1306_ADDRESS = 0x3c
MQTT_BROKER=b"192.168.50.6"


# initialize display so can display network status
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
bme = bme280.BME280(i2c=i2c, address=I2C_BME280_ADDRESS)
display = SSD1306_I2C(128, 32, i2c, addr=I2C_SSD1306_ADDRESS)

dot_position = 0
dot_incr = 6

ssid = 'SSID'
password = 'password'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


display.fill(0)
display.text("Waiting on WiFi", 3, 0, 1)
display.show()

# Wait for connect or fail
max_wait = 10

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
sleep(2)


def connectMQTT():
    client = MQTTClient(client_id=b"picow0_bme280",
                        server=MQTT_BROKER,
                        #port=1883,
                        #user=b"mydemoclient",
                        #password=b"passowrd",
                        keepalive=7200,
                        # ssl=False, #ssl=True,
                        )

    client.connect()
    return client


client = connectMQTT()


def publish(topic, value):
    # print(topic, value)
    client.publish(topic, value)
    # print("publish Done",)


while True:
    sensor_reading = bme
    temperature = sensor_reading.values[0]
    pressure = sensor_reading.values[1]
    humidity = sensor_reading.values[2]

    print(sensor_reading.values)

    # publish as MQTT payload
    publish('picow0/temperature', temperature)
    publish('picow0/pressure', pressure)
    publish('picow0/humidity', humidity)

    # show on display
    display.fill(0)
    display.text("Temp " + bme.values[0], 3, 0, 1)
    display.text("PA  " + bme.values[1], 3, 11, 1)
    display.text("Humidity " + bme.values[2], 3, 23, 1)
    display.show()

    # delay 5 seconds
    sleep(5)
