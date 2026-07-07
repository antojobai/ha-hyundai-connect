"""Hyundai/Kia Connect main integration file."""
from __future__ import annotations

from datetime import timedelta
import logging

from hyundai_kia_connect_api import (
    OTP_NOTIFY_TYPE,
    VehicleManager,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_PIN,
    CONF_REGION,
    CONF_USERNAME,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    CONF_BRAND,
    DOMAIN,
    PLATFORMS,
    UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    hass.data.setdefault(DOMAIN, {})
    car_data = HyundaikiaData(hass, entry)
    try:
        await car_data.async_start_scanning()
    except Exception as exc:
        error_msg = str(exc).lower()
        if "incorrect username or password" in error_msg or "authentication failed" in error_msg:
            raise ConfigEntryAuthFailed from exc
        raise ConfigEntryNotReady(str(exc)) from exc

    hass.data[DOMAIN][entry.entry_id] = car_data
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    _register_services(hass, car_data)

    return True


UNREGISTER_LISTENER = "hyundai_kia_connect_unregister_listener"


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if entry.entry_id in hass.data[DOMAIN]:
        await hass.data[DOMAIN][entry.entry_id].coordinator.async_shutdown()
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    returned = unload_ok
    if UNREGISTER_LISTENER in hass.data:
        unregister = hass.data.pop(UNREGISTER_LISTENER)
        unregister()
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return returned


def _register_services(hass: HomeAssistant, car_data: HyundaikiaData) -> None:
    """Register custom services."""

    async def handle_lock(call):
        """Service handler to lock the vehicle."""
        car_data.manager.lock()

    async def handle_unlock(call):
        """Service handler to unlock the vehicle."""
        car_data.manager.unlock()

    async def handle_start_climate(call):
        """Service handler to start climate control."""
        temperature = call.data.get("temperature", 21)
        duration = call.data.get("duration", 5)
        defrost = call.data.get("defrost", False)
        climate = call.data.get("climate", True)
        heating = call.data.get("heating", 0)
        from hyundai_kia_connect_api import ClimateRequestOptions
        car_data.manager.start_climate(
            ClimateRequestOptions(
                set_temp=temperature,
                duration=duration,
                defrost=defrost,
                climate=climate,
                heating=heating,
            )
        )

    async def handle_stop_climate(call):
        """Service handler to stop climate control."""
        car_data.manager.stop_climate()

    async def handle_locate(call):
        """Service handler to locate the vehicle."""
        car_data.manager.locate_vehicle()

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["services_registered"] = True

    if not hass.services.has_service(DOMAIN, "lock"):
        hass.services.async_register(DOMAIN, "lock", handle_lock)
    if not hass.services.has_service(DOMAIN, "unlock"):
        hass.services.async_register(DOMAIN, "unlock", handle_unlock)
    if not hass.services.has_service(DOMAIN, "start_climate"):
        hass.services.async_register(DOMAIN, "start_climate", handle_start_climate)
    if not hass.services.has_service(DOMAIN, "stop_climate"):
        hass.services.async_register(DOMAIN, "stop_climate", handle_stop_climate)
    if not hass.services.has_service(DOMAIN, "locate"):
        hass.services.async_register(DOMAIN, "locate", handle_locate)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


class HyundaikiaData:
    """Container for the VehicleManager API client and update coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.hass = hass
        self.config_entry = entry
        self.manager = VehicleManager(
            region=entry.data[CONF_REGION],
            brand=entry.data[CONF_BRAND],
            username=entry.data[CONF_USERNAME],
            password=entry.data[CONF_PASSWORD],
            pin=entry.data.get(CONF_PIN),
        )
        self.coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_method=self._async_update,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def async_start_scanning(self) -> None:
        """Initial scan."""
        try:
            result = await self.hass.async_add_executor_job(self.manager.login)
            if result is not True:
                raise Exception("Login failed")
            await self.hass.async_add_executor_job(
                self.manager.update_all_vehicles_with_cached_state
            )
            await self.coordinator.async_refresh()
        except Exception as exc:
            _LOGGER.exception("Error during initial scan: %s", exc)
            raise

    async def _async_update(self) -> None:
        """Poll all exposed API endpoints via VehicleManager."""
        await self.hass.async_add_executor_job(
            self.manager.check_and_force_update_vehicles,
            int(timedelta(seconds=UPDATE_INTERVAL).total_seconds()),
        )

    def get_vehicles(self):
        """Return the VehicleManager instance."""
        return self.manager
