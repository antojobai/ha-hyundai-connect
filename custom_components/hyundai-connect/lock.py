"""Lock platform for Hyundai/Kia Connect."""
from __future__ import annotations

from homeassistant.components.lock import (
    LockDeviceClass,
    LockEntity,
    LockEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import HyundaikiaData
from .const import DOMAIN
from .entity import HyundaikiaEntity

PARALLEL_UPDATES = 1


LOCK_TYPES: tuple[LockEntityDescription, ...] = (
    LockEntityDescription(
        key="is_locked",
        translation_key="is_locked",
        device_class=LockDeviceClass.DOOR,
        name="Door Lock",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Hyundai/Kia Connect locks."""
    car_data: HyundaikiaData = hass.data[DOMAIN][entry.entry_id]
    vehicles = car_data.get_vehicles()
    entities = []
    for vehicle_id, vehicle in vehicles.items():
        for description in LOCK_TYPES:
            entities.append(HyundaikiaLock(car_data, vehicle, vehicle_id, description))
    async_add_entities(entities)


class HyundaikiaLock(HyundaikiaEntity, LockEntity):
    """Representation of a Hyundai/Kia Connect Lock."""

    def __init__(
        self,
        car_data: HyundaikiaData,
        vehicle,
        unique_prefix: str,
        description: LockEntityDescription,
    ) -> None:
        super().__init__(car_data, vehicle, unique_prefix, description.key)
        self.entity_description = description

    @property
    def is_locked(self):
        """Return the state of the lock."""
        val = getattr(self.vehicle, self.translation_key, None)
        if val is None:
            return None
        if isinstance(val, bool):
            return val
        return bool(val)

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        if not self.vehicle.enabled:
            return False
        return True

    async def async_lock(self, **kwargs) -> None:
        """Lock the vehicle."""
        self.manager.lock(self.vehicle.id)

    async def async_unlock(self, **kwargs) -> None:
        """Unlock the vehicle."""
        self.manager.unlock(self.vehicle.id)
