from machine import Pin, I2C
import network
from time import sleep
import bme280
from umqtt.simple import MQTTClient

# subscribe topic picow/# on http://192.168.50.6:9001/ (ws server configured)

ssid = 'SSID'
password = 'wifipassword'
mqtt_broker=b"192.168.50.6"

I2C_BME280_ADDRESS = 0x77

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


# Wait for connect or fail
max_wait = 10
while max_wait > 0:

    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')

status = wlan.ifconfig()
print('ip = ' + status[0])

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
bme = bme280.BME280(i2c=i2c, address=I2C_BME280_ADDRESS)

print(bme.values)


def connectMQTT():
    client = MQTTClient(client_id=b"picow_go_moo_raspberries",
                        server=mqtt_broker,
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
    publish('picow/temperature', temperature)
    publish('picow/pressure', pressure)
    publish('picow/humidity', humidity)
    # delay 5 seconds
    sleep(5)
