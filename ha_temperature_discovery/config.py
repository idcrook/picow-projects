# import re

from device import ONEWIRE_CONFIG, I2C_CONFIG, APP_CONFIG

def unique_device_identifier(mac_addr_hexlified):
    """Use MAC address to generate a unique string for this device."""
    # Let's start with last three nibbles of MAC address
    trailing_nibbles = mac_addr_hexlified.replace(":", "")[-3:]
    return trailing_nibbles


SWVER = "0.1"
HWVER = "0.1"
MDL = "Pico temp"
MNF = "idcrook-labs"
DEV = "seedomatic"
NAME = f"{MNF} {MDL}"

CFG_DEV = {
    "sw": SWVER,
    "hw": HWVER,
    "mdl": MDL,
    "mf": MNF,
    "name": NAME,
    "ids": [],
}

def set_mqtt_disc_dev_id(identifiers):
    if isinstance(identifiers, list):
        CFG_DEV['ids'] = identifiers
    elif isinstance(identifiers, tuple):
        CFG_DEV['ids'] = list(*identifiers)
    else:
        CFG_DEV['ids'] = [identifiers]
