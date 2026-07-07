"""Device tracker platform for Hyundai/Kia Connect."""
from __future__ import annotations

from homeassistant.components.device_tracker import (
    DeviceTrackerEntity,
    DeviceTrackerEntityDescription,
    SourceType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import HyundaikiaData
from .const import DOMAIN
from .entity import HyundaikiaEntity

PARALLEL_UPDATES = 1

DEVICE_TRACKER_TYPES: tuple[DeviceTrackerEntityDescription, ...] = (
    DeviceTrackerEntityDescription(
        key="location",
        translation_key="location",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Hyundai/Kia Connect device tracker."""
    car_data: HyundaikiaData = hass.data[DOMAIN][entry.entry_id]
    vehicles = car_data.get_vehicles()
    entities = []
    for vehicle_id, vehicle in vehicles.items():
        for description in DEVICE_TRACKER_TYPES:
            entities.append(
                HyundaikiaDeviceTracker(car_data, vehicle, vehicle_id, description)
            )
    async_add_entities(entities)


class HyundaikiaDeviceTracker(HyundaikiaEntity, DeviceTrackerEntity):
    """Representation of a Hyundai/Kia Connect Device Tracker."""

    _attr_source_type = SourceType.GPS
    _attr_icon = "mdi:car"

    def __init__(
        self,
        car_data: HyundaikiaData,
        vehicle,
        unique_prefix: str,
        description: DeviceTrackerEntityDescription,
    ) -> None:
        super().__init__(car_data, vehicle, unique_prefix, description.key)
        self.entity_description = description

    @property
    def latitude(self):
        """Return the latitude of the vehicle."""
        return self.vehicle.location_latitude

    @property
    def longitude(self):
        """Return the longitude of the vehicle."""
        return self.vehicle.location_longitude

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        if not self.vehicle.enabled:
            return False
        return (
            self.vehicle.location_latitude is not None
            and self.vehicle.location_longitude is not None
        )
