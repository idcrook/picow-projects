import re

from device import ONEWIRE_CONFIG, I2C_CONFIG, APP_CONFIG

def unique_device_identifier(mac_addr_hexlified):
    "Use MAC address to generate a unique string for this device."

    global UDI
    # Let's start with last three nibbles of MAC address
    trailing_nibbles = mac_addr_hexlified.replace(":", "")[-3:]
    return trailing_nibbles


def init():
    dev_id = APP_CONFIG.setdefault("device_name", "picow999")


# # FIXME: generate from device MAC, say trailing 3 nibbles
# UNIQUE_ID_PRE = "940"

# VER = "0.1"
# MDL = "Pico W temp humid"
# MNF = "idcrook"
# AREA = "Bedroom 2"
# DEV = "seedomatic"
# NAME = f"{MNF} {MDL}"

# ID = f"{DEV}_{UNIQUE_ID_PRE}"

# ST_BASE = f"{ID}/status"
# CMD_TPC = f"{ID}/command"
# AV_TPC = ST_BASE + "/availability"
# ST_TPC = ST_BASE + "/readings"

# CFG_DEV = {
#     "sw": VER,
#     "mdl": MDL,
#     "mf": MNF,
#     "sa": AREA,
#     "name": NAME,
#     "ids": [ID],
# }


# BASE_CFG = {
#     "~": ID,
#     "state_topic": "~/status/readings",
#     "avty_t": "~/status/availability",
#     "device": CFG_DEV,
# }

# COMPONENTS = {
#     "bed1": {
#         "p": "sensor",
#         "dev_cla": "temperature",
#         "uniq_id": UNIQUE_ID_PRE + "_bed1",
#         "val_tpl": "{{ value_json.probe1_temp }}",
#         "unit_of_meas": "C",
#     },
#     "bed2": {
#         "p": "sensor",
#         "dev_cla": "temperature",
#         "uniq_id": UNIQUE_ID_PRE + "_bed2",
#         "val_tpl": "{{ value_json.probe2_temp }}",
#         "unit_of_meas": "C",
#     },
#     "env_temperature": {
#         "p": "sensor",
#         "dev_cla": "temperature",
#         "uniq_id": UNIQUE_ID_PRE + "_env_t",
#         "val_tpl": "{{ value_json.env_temp }}",
#         "unit_of_meas": "C",
#     },
#     "env_humidity": {
#         "name": "Air Quality Index",
#         "p": "sensor",
#         "dev_cla": "humidity",
#         "uniq_id": UNIQUE_ID_PRE + "_env_h",
#         "val_tpl": "{{ value_json.env_humidity }}",
#         "unit_of_meas": "",
#     },
# }
