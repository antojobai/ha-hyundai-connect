from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import AbortFlow

from .const import (
    BRANDS,
    CONF_BRAND,
    CONF_PASSWORD,
    CONF_PIN,
    CONF_REGION,
    CONF_USERNAME,
    DEFAULT_BRAND,
    DEFAULT_PIN,
    DEFAULT_REGION,
    DOMAIN,
    REGIONS,
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_REGION, default=DEFAULT_REGION): vol.In(REGIONS),
        vol.Required(CONF_BRAND, default=DEFAULT_BRAND): vol.In(BRANDS),
        vol.Required(CONF_PIN, default=DEFAULT_PIN): str,
    }
)


class HyundaiKiaConnectConfigFlow(ConfigFlow, domain=DOMAIN):
    """Hyundai/Kia Connect config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                return await self._test_credentials(user_input)
            except AbortFlow:
                raise
            except Exception as exc:  # pylint: disable=broad-except
                error_msg = str(exc).lower()
                if "incorrect username or password" in error_msg:
                    errors["base"] = "invalid_auth"
                elif "authentication failed" in error_msg:
                    errors["base"] = "invalid_auth"
                elif "login failed" in error_msg:
                    errors["base"] = "invalid_auth"
                else:
                    _LOGGER.exception(
                        "Unexpected exception during config flow validation: %s", exc
                    )
                    errors["base"] = "unknown"
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def _test_credentials(self, user_input: dict[str, Any]) -> ConfigFlowResult:
        from hyundai_kia_connect_api import (
            VehicleManager,
            AuthenticationOTPRequired as _AuthOTP,
        )
        manager = VehicleManager(
            region=user_input[CONF_REGION],
            brand=user_input[CONF_BRAND],
            username=user_input[CONF_USERNAME],
            password=user_input[CONF_PASSWORD],
            pin=user_input.get(CONF_PIN),
        )
        result = await self.hass.async_add_executor_job(manager.login)
        if isinstance(result, _AuthOTP):
            # OTP flow not supported in this version of config flow, treat as auth needed
            return self.async_abort(reason="invalid_auth")
        unique_id = user_input[CONF_USERNAME]
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_updated()
        title = user_input[CONF_USERNAME]
        return self.async_create_entry(title=title, data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Return the options flow."""
        return HyundaiKiaConnectOptionsFlow(config_entry)


class HyundaiKiaConnectOptionsFlow(OptionsFlow):
    """Handle options flow."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Handle options init step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_PIN, default=self.config_entry.data.get(CONF_PIN, DEFAULT_PIN)): str,
                    vol.Optional(CONF_PASSWORD, default=self.config_entry.data.get(CONF_PASSWORD, "")): str,
                    vol.Optional(CONF_USERNAME, default=self.config_entry.data.get(CONF_USERNAME, "")): str,
                }
            ),
            errors=errors,
        )
