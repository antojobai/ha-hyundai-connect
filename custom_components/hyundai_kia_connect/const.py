from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "hyundai_kia_connect"

CONF_BRAND = "brand"
CONF_PIN = "pin"
CONF_REGION = "region"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

DEFAULT_BRAND = 2
DEFAULT_REGION = 6
DEFAULT_PIN = "3011"
BRANDS = {
    1: "Kia",
    2: "Hyundai",
    3: "Genesis",
}
REGIONS = {
    1: "Europe",
    2: "Canada",
    3: "USA",
    4: "China",
    5: "Australia",
    6: "India",
    7: "New Zealand",
    8: "Brazil",
}

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CLIMATE,
    Platform.DEVICE_TRACKER,
    Platform.LOCK,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
]

UPDATE_INTERVAL = 30  # seconds
