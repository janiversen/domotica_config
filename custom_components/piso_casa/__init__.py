""" piso and casa"""

from homeassistant.helpers.discovery import async_load_platform
from homeassistant.const import Platform

from .base import _LOGGER, DOMAIN

async def async_setup(hass, _config):
    """Prepare piso/casa automations."""
    casa = _config[DOMAIN]
    hass.data[DOMAIN] = casa
    hass.async_create_task(
        async_load_platform(hass, Platform.SENSOR, DOMAIN, casa, {})
    )
    hass.async_create_task(
        async_load_platform(hass, Platform.SWITCH, DOMAIN, casa, {})
    )
    return True
