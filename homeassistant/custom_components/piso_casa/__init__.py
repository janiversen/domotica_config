"""piso and casa"""

from homeassistant.const import Platform
from homeassistant.helpers.discovery import async_load_platform

from .base import DOMAIN, _LOGGER
from .trigger import triggers


async def async_setup(hass, _config):
    """Prepare piso/casa automations."""
    _LOGGER.setLevel("DEBUG")
    _LOGGER.debug("Piso/Casa automation starting")
    _LOGGER.debug(f"JAN --> {_config}")
    casa = _config[DOMAIN]
    hass.data[DOMAIN] = casa
    hass.async_create_task(
        async_load_platform(hass, Platform.SENSOR, DOMAIN, casa, {})
    )
    hass.async_create_task(
        async_load_platform(hass, Platform.SWITCH, DOMAIN, casa, {})
    )
    triggers(hass, casa)
    return True
