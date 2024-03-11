import asyncio
from datetime import datetime

from homeassistant.core import callback
from homeassistant.helpers.event import (
    async_track_state_change_event,
)
from .base import _LOGGER


class triggers:
    """Handle triggers without sensor."""

    last_switch = None
    hass = None
    is_casa = False

    def __init__(self, hass, casa):
        """Prepare class"""
        self.hass = hass
        self.is_casa = casa["casa"]
        async_track_state_change_event(
            hass, ["switch.calentador"], self.async_track_boiler
        )


    @callback
    def async_track_boiler(self, event) -> None:
        """Track boiler on/off."""
        if event.data["new_state"].state != "on":
            return
        if (self.hass.states.get("switch.vamos_a_estar").state == "on"):
            asyncio.run_coroutine_threadsafe(
                self.hass.services.async_call(
                    "switch",
                    "turn_off",
                    {"entity_id": "switch.vamos_a_estar"},
                    blocking=True,
                ),
                self.hass.loop
            )
            return
        if (
            self.hass.states.get("person.jan").state == "home" or
            self.hass.states.get("person.belen").state == "home" or
            self.hass.states.get("switch.vamos_a_estar").state == "on"
        ):
            return
        asyncio.run_coroutine_threadsafe(
            self.hass.services.async_call(
                "switch",
                "turn_off",
                {"entity_id": "switch.calentador"},
                blocking=True,
            ),
            self.hass.loop
        )
