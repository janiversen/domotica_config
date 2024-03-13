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
    jan_belen = [False] * 5

    def __init__(self, hass, casa):
        """Prepare class"""
        self.hass = hass
        self.is_casa = casa["casa"]
        async_track_state_change_event(
            hass, ["device_tracker.jan_ipad_casa"], partial(self.track_home, 1)
        )
        async_track_state_change_event(
            hass, ["device_tracker.jan_ipad_piso"], partial(self.track_home, 2)
        )
        async_track_state_change_event(
            hass, ["device_tracker.belen_ipad_casa"], partial(self.track_home, 3)
        )
        async_track_state_change_event(
            hass, ["device_tracker.belen_ipad_piso"], partial(self.track_home, 4)
        )
        if self.is_casa:
            async_track_state_change_event(
                hass, ["switch.calentador"], self.track_boiler
            )


    @callback
    def track_boiler(self, event) -> None:
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
            self.jan_belen[1] or
            self.jan_belen[3] or
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


    @callback
    def track_home(self, inx, event) -> None:
        """Track jan/belen in casa/piso/away."""
        state = event.data["new_state"].state
        self.jan_belen[inx] = True if state == "home" else False
        if inx < 3:
            offset = 1
            entity = "person.jan"
        else:
            offset = 3
            entity = "person.belen"

        if self.jan_belen[offset]:
            state = "Casa"
        elif self.jan_belen[offset+1]:
            state = "Piso"
        else:
            state = "Fuera"
        before = self.hass.states.get(entity)
        before_state = before.state
        self.hass.states.async_set(entity, state, {})
        x_state = self.hass.states.get(entity)
        new_state = x_state.state
        _LOGGER.debug(f"--> JAN PERSON before {entity} before({before}) new({x_state})")

        _LOGGER.debug(f"--> JAN PERSON {entity}={state} before({before_state}) new({new_state})")
