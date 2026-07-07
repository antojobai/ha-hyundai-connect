"""Base entity for Hyundai/Kia Connect."""
from __future__ import annotations

from typing import Any

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from . import HyundaikiaData


class HyundaikiaEntity(CoordinatorEntity):
    """Base class for Hyundai/Kia Connect entities."""

    _attr_should_poll = True

    def __init__(
        self,
        car_data: HyundaikiaData,
        vehicle,
        unique_prefix: str,
        key: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(car_data.coordinator)
        self._vehicle = vehicle
        self._key = key
        self._attr_unique_id = f"{unique_prefix}_{key}"
        self._attr_device_info = {
            "identifiers": {("hyundai_kia_connect", unique_prefix)},
            "name": vehicle.name,
            "manufacturer": "Hyundai",
            "model": vehicle.model,
            "sw_version": str(getattr(vehicle, "VIN", "")),
        }

    @property
    def vehicle(self):
        """Return the vehicle object."""
        return self._vehicle

    @property
    def translation_key(self) -> str:
        """Return the translation key."""
        return self._key

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        if not self._vehicle.enabled:
            return False
        val = getattr(self._vehicle, self._key, None)
        if val is not None:
            return True
        if self._key in ("last_updated_at", "last_scanned_at"):
            return True
        return self.coordinator.last_update_success
