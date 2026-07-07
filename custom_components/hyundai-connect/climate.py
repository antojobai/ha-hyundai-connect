"""Climate platform for Hyundai/Kia Connect."""
from __future__ import annotations

from homeassistant.components.climate import (
    ATTR_TEMPERATURE,
    ClimateEntity,
    ClimateEntityDescription,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import HyundaikiaData
from .const import DOMAIN
from .entity import HyundaikiaEntity

PARALLEL_UPDATES = 1

CLIMATE_TYPES: tuple[ClimateEntityDescription, ...] = (
    ClimateEntityDescription(
        key="climate",
        translation_key="climate",
        name="Climate",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Hyundai/Kia Connect climate entities."""
    car_data: HyundaikiaData = hass.data[DOMAIN][entry.entry_id]
    vehicles = car_data.get_vehicles()
    entities = []
    for vehicle_id, vehicle in vehicles.items():
        for description in CLIMATE_TYPES:
            entities.append(
                HyundaikiaClimate(car_data, vehicle, vehicle_id, description)
            )
    async_add_entities(entities)


class HyundaikiaClimate(HyundaikiaEntity, ClimateEntity):
    """Representation of a Hyundai/Kia Climate Control."""

    def __init__(
        self,
        car_data: HyundaikiaData,
        vehicle,
        unique_prefix: str,
        description: ClimateEntityDescription,
    ) -> None:
        super().__init__(car_data, vehicle, unique_prefix, description.key)
        self.entity_description = description
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_min_temp = 16.0
        self._attr_max_temp = 30.0
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
        self._attr_supported_features = ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF | ClimateEntityFeature.TARGET_TEMPERATURE
        self._attr_hvac_mode = HVACMode.OFF

    @property
    def hvac_mode(self) -> HVACMode:
        """Return the current HVAC mode."""
        if self.vehicle.air_control_is_on or self.vehicle.engine_is_running:
            return HVACMode.HEAT
        return HVACMode.OFF

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        if self.vehicle.air_temperature is not None:
            try:
                return float(self.vehicle.air_temperature)
            except (ValueError, TypeError):
                return None
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        if self.vehicle.air_temperature is not None:
            try:
                return float(self.vehicle.air_temperature)
            except (ValueError, TypeError):
                return None
        return None

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set the HVAC mode."""
        if hvac_mode == HVACMode.HEAT:
            await self._start_climate()
        if hvac_mode == HVACMode.OFF:
            await self._stop_climate()

    async def async_set_temperature(self, **kwargs) -> None:
        """Set the target temperature."""
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is not None:
            await self._start_climate(target_temp)

    async def _start_climate(self, target_temp: float = 21.0) -> None:
        """Start climate control."""
        from hyundai_kia_connect_api import ClimateRequestOptions
        options = ClimateRequestOptions(
            set_temp=target_temp, duration=5, defrost=False, climate=True, heating=0
        )
        self.manager.start_climate(self.vehicle.id, options)

    async def _stop_climate(self) -> None:
        """Stop climate control."""
        self.manager.stop_climate(self.vehicle.id)
