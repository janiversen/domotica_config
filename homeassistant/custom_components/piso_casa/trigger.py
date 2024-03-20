import asyncio
from datetime import datetime
from functools import partial

from homeassistant.core import callback
from homeassistant.helpers.event import (
    async_track_state_change_event,
)
from .base import _LOGGER


class triggers:
    """Handle triggers without sensor."""

    hass = None
    is_casa = False
    jan_belen = [False] * 4

    def __init__(self, hass, casa):
        """Prepare class"""
        self.hass = hass
        self.is_casa = casa["casa"]
        tracker = (
            "device_tracker.jan_ipad_casa",
            "device_tracker.jan_ipad_piso",
            "device_tracker.belen_ipad_casa",
            "device_tracker.belen_ipad_piso",
        )
        for i in range(4):
            async_track_state_change_event(
                hass, [tracker[i]], partial(self.track_home, i)
            )
            self.jan_belen[i] = (self.hass.states.get(tracker[i]).state == "home")
        self.hass.loop.call_soon_threadsafe(self.set_home, 0)
        self.hass.loop.call_soon_threadsafe(self.set_home, 2)

    @callback
    def track_boiler(self, event) -> None:
        """Track boiler on/off."""
        if event.data["new_state"].state != "on":
            return
        is_vamos = (self.hass.states.get("switch.vamos_a_estar").state == "on")
        if is_vamos:
            asyncio.run_coroutine_threadsafe(
                self.hass.services.async_call(
                    "switch",
                    "turn_off",
                    {"entity_id": "switch.vamos_a_estar"},
                    blocking=True,
                ),
                self.hass.loop
            )
        if (
            self.jan_belen[0] or
            self.jan_belen[2] or
            is_vamos
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


    @callback
    def track_home(self, inx, event) -> None:
        """Track jan/belen in casa/piso/away."""
        self.jan_belen[inx] = (event.data["new_state"].state == "home")
        self.set_home(inx)

    def set_home(self, inx):
        """Set home if so."""
        if inx < 2:
            offset = 0
            entity = "person.jan"
        else:
            offset = 2
            entity = "person.belen"

        if self.jan_belen[offset]:
            state = "Casa"
        elif self.jan_belen[offset+1]:
            state = "Piso"
        else:
            state = "Fuera"
        old_state = self.hass.states.get(entity)
        self.hass.states.async_set(entity, state, old_state.attributes)
