"""Binary sensor platform for Hyundai/Kia Connect."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import HyundaikiaData
from .const import DOMAIN
from .entity import HyundaikiaEntity

PARALLEL_UPDATES = 1


BINARY_SENSOR_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="is_locked",
        translation_key="is_locked",
        device_class=BinarySensorDeviceClass.LOCK,
    ),
    BinarySensorEntityDescription(
        key="front_left_door_is_open",
        translation_key="front_left_door_is_open",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDescription(
        key="front_right_door_is_open",
        translation_key="front_right_door_is_open",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDescription(
        key="back_left_door_is_open",
        translation_key="back_left_door_is_open",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDescription(
        key="back_right_door_is_open",
        translation_key="back_right_door_is_open",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDescription(
        key="trunk_is_open",
        translation_key="trunk_is_open",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDescription(
        key="hood_is_open",
        translation_key="hood_is_open",
        device_class=BinarySensorDeviceClass.DOOR,
    ),
    BinarySensorEntityDescription(
        key="front_left_window_is_open",
        translation_key="front_left_window_is_open",
        device_class=BinarySensorDeviceClass.WINDOW,
    ),
    BinarySensorEntityDescription(
        key="front_right_window_is_open",
        translation_key="front_right_window_is_open",
        device_class=BinarySensorDeviceClass.WINDOW,
    ),
    BinarySensorEntityDescription(
        key="back_left_window_is_open",
        translation_key="back_left_window_is_open",
        device_class=BinarySensorDeviceClass.WINDOW,
    ),
    BinarySensorEntityDescription(
        key="back_right_window_is_open",
        translation_key="back_right_window_is_open",
        device_class=BinarySensorDeviceClass.WINDOW,
    ),
    BinarySensorEntityDescription(
        key="defrost_is_on",
        translation_key="defrost_is_on",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="steering_wheel_heater_is_on",
        translation_key="steering_wheel_heater_is_on",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="back_window_heater_is_on",
        translation_key="back_window_heater_is_on",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="air_control_is_on",
        translation_key="air_control_is_on",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="accessory_on",
        translation_key="accessory_on",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="ign3",
        translation_key="ign3",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="sleep_mode_check",
        translation_key="sleep_mode_check",
        device_class=BinarySensorDeviceClass.POWER,
    ),
    BinarySensorEntityDescription(
        key="fuel_level_is_low",
        translation_key="fuel_level_is_low",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="washer_fluid_warning_is_on",
        translation_key="washer_fluid_warning_is_on",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="brake_fluid_warning_is_on",
        translation_key="brake_fluid_warning_is_on",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="smart_key_battery_warning_is_on",
        translation_key="smart_key_battery_warning_is_on",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="headlamp_status",
        translation_key="headlamp_status",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="headlamp_left_low",
        translation_key="headlamp_left_low",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="headlamp_right_low",
        translation_key="headlamp_right_low",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="headlamp_left_high",
        translation_key="headlamp_left_high",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="headlamp_right_high",
        translation_key="headlamp_right_high",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="headlamp_left_bifunc",
        translation_key="headlamp_left_bifunc",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="headlamp_right_bifunc",
        translation_key="headlamp_right_bifunc",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="stop_lamp_left",
        translation_key="stop_lamp_left",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="stop_lamp_right",
        translation_key="stop_lamp_right",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="turn_signal_left_front",
        translation_key="turn_signal_left_front",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="turn_signal_right_front",
        translation_key="turn_signal_right_front",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="turn_signal_left_rear",
        translation_key="turn_signal_left_rear",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="turn_signal_right_rear",
        translation_key="turn_signal_right_rear",
        device_class=BinarySensorDeviceClass.LIGHT,
    ),
    BinarySensorEntityDescription(
        key="valet_mode_active",
        translation_key="valet_mode_active",
        device_class=BinarySensorDeviceClass.RUNNING,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Hyundai/Kia Connect binary sensors."""
    car_data: HyundaikiaData = hass.data[DOMAIN][entry.entry_id]
    vehicles = car_data.get_vehicles()
    entities = []
    for vehicle_id, vehicle in vehicles.items():
        for description in BINARY_SENSOR_TYPES:
            entities.append(HyundaikiaBinarySensor(car_data, vehicle, vehicle_id, description))
    async_add_entities(entities)


class HyundaikiaBinarySensor(HyundaikiaEntity, BinarySensorEntity):
    """Representation of a Hyundai/Kia Connect Binary Sensor."""

    def __init__(
        self,
        car_data: HyundaikiaData,
        vehicle,
        unique_prefix: str,
        description: BinarySensorEntityDescription,
    ) -> None:
        super().__init__(car_data, vehicle, unique_prefix, description.key)
        self.entity_description = description

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        val = getattr(self.vehicle, self.translation_key, None)
        if val is None:
            return None
        if isinstance(val, int):
            return bool(val)
        return bool(val)

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        if not self.vehicle.enabled:
            return False
        if self.translation_key == "valet_mode_active":
            return getattr(self.vehicle, "supports_valet_mode", False) is True
        if self.translation_key in (
            "back_left_window_is_open", "back_right_window_is_open",
            "front_left_window_is_open", "front_right_window_is_open",
        ):
            return getattr(self.vehicle, "supports_window_control", False) is True
        return super().available
