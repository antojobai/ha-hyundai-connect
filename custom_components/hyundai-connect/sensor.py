"""Sensor platform for Hyundai/Kia Connect."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfLength, UnitOfPower, UnitOfTime, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util.dt import as_local

from . import HyundaikiaData
from .const import DOMAIN
from .entity import HyundaikiaEntity

PARALLEL_UPDATES = 1


SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="last_updated_at",
        translation_key="last_updated_at",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:clock",
    ),
    SensorEntityDescription(
        key="last_scanned_at",
        translation_key="last_scanned_at",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:clock",
    ),
    SensorEntityDescription(
        key="odometer",
        translation_key="odometer",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="engine_is_running",
        translation_key="engine_is_running",
        device_class=None,
        icon="mdi:engine",
    ),
    SensorEntityDescription(
        key="air_temperature",
        translation_key="air_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="fuel_level",
        translation_key="fuel_level",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=0,
        icon="mdi:gas-station",
    ),
    SensorEntityDescription(
        key="fuel_driving_range",
        translation_key="fuel_driving_range",
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:map-marker-distance",
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="fuel_level_is_low",
        translation_key="fuel_level_is_low",
        device_class=None,
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="defrost_is_on",
        translation_key="defrost_is_on",
        device_class=None,
        icon="mdi:car-defrost",
    ),
    SensorEntityDescription(
        key="air_control_is_on",
        translation_key="air_control_is_on",
        device_class=None,
        icon="mdi:air-conditioner",
    ),
    SensorEntityDescription(
        key="steering_wheel_heater_is_on",
        translation_key="steering_wheel_heater_is_on",
        device_class=None,
        icon="mdi:steering",
    ),
    SensorEntityDescription(
        key="back_window_heater_is_on",
        translation_key="back_window_heater_is_on",
        device_class=None,
        icon="mdi:car-defrost-rear",
    ),
    SensorEntityDescription(
        key="front_left_seat_status",
        translation_key="front_left_seat_status",
        device_class=None,
        icon="mdi:car-seat-heater",
    ),
    SensorEntityDescription(
        key="front_right_seat_status",
        translation_key="front_right_seat_status",
        device_class=None,
        icon="mdi:car-seat-heater",
    ),
    SensorEntityDescription(
        key="rear_left_seat_status",
        translation_key="rear_left_seat_status",
        device_class=None,
        icon="mdi:car-seat-heater",
    ),
    SensorEntityDescription(
        key="rear_right_seat_status",
        translation_key="rear_right_seat_status",
        device_class=None,
        icon="mdi:car-seat-heater",
    ),
    SensorEntityDescription(
        key="tire_pressure_all_warning_is_on",
        translation_key="tire_pressure_all_warning_is_on",
        device_class=None,
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="tire_pressure_rear_left_warning_is_on",
        translation_key="tire_pressure_rear_left_warning_is_on",
        device_class=None,
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="tire_pressure_front_left_warning_is_on",
        translation_key="tire_pressure_front_left_warning_is_on",
        device_class=None,
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="tire_pressure_front_right_warning_is_on",
        translation_key="tire_pressure_front_right_warning_is_on",
        device_class=None,
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="tire_pressure_rear_right_warning_is_on",
        translation_key="tire_pressure_rear_right_warning_is_on",
        device_class=None,
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="washer_fluid_warning_is_on",
        translation_key="washer_fluid_warning_is_on",
        device_class=None,
        icon="mdi:wiper",
    ),
    SensorEntityDescription(
        key="brake_fluid_warning_is_on",
        translation_key="brake_fluid_warning_is_on",
        device_class=None,
        icon="mdi:car-brake-alert",
    ),
    SensorEntityDescription(
        key="smart_key_battery_warning_is_on",
        translation_key="smart_key_battery_warning_is_on",
        device_class=None,
        icon="mdi:key-variant",
    ),
    SensorEntityDescription(
        key="accessory_on",
        translation_key="accessory_on",
        device_class=None,
        icon="mdi:power-socket-eu",
    ),
    SensorEntityDescription(
        key="ign3",
        translation_key="ign3",
        device_class=None,
        icon="mdi:power",
    ),
    SensorEntityDescription(
        key="transmission_condition",
        translation_key="transmission_condition",
        device_class=None,
        icon="mdi:car-shift",
    ),
    SensorEntityDescription(
        key="sleep_mode_check",
        translation_key="sleep_mode_check",
        device_class=None,
        icon="mdi:sleep",
    ),
    SensorEntityDescription(
        key="dtc_count",
        translation_key="dtc_count",
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        icon="mdi:alert-octagon",
    ),
    SensorEntityDescription(
        key="valet_mode_active",
        translation_key="valet_mode_active",
        device_class=None,
        icon="mdi:car",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Hyundai/Kia Connect sensors."""
    car_data: HyundaikiaData = hass.data[DOMAIN][entry.entry_id]
    vehicles = car_data.get_vehicles()
    entities = []
    for vehicle_id, vehicle in vehicles.items():
        for description in SENSOR_TYPES:
            entities.append(HyundaikiaSensor(car_data, vehicle, vehicle_id, description))
    async_add_entities(entities)


class HyundaikiaSensor(HyundaikiaEntity, SensorEntity):
    """Representation of a Hyundai/Kia Connect Sensor."""

    def __init__(
        self,
        car_data: HyundaikiaData,
        vehicle,
        unique_prefix: str,
        description: SensorEntityDescription,
    ) -> None:
        super().__init__(car_data, vehicle, unique_prefix, description.key)
        self.entity_description = description
        self._attr_name = f"{vehicle.name} {description.key.replace('_', ' ').title()}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        val = getattr(self.vehicle, self.translation_key, None)
        if val is None and self.translation_key == "last_scanned_at":
            val = self.vehicle.last_scanned_at
        if val is None and self.translation_key == "last_updated_at":
            val = self.vehicle.last_updated_at
        if hasattr(val, "total_seconds"):
            return as_local(val) if self.entity_description.device_class == SensorDeviceClass.TIMESTAMP and val else val
        return val
