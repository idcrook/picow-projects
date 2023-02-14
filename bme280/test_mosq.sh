#!/bin/bash -x

# assumes a MQTT broker is configured and accessible
# needs the mosquitto clients installed

# sudo apt install mosquitto-clients

server=192.168.50.6
message="test1"
topic="picow/temperature"

mosquitto_pub -h "${server}"  -m "${message}" -t "${topic}"
