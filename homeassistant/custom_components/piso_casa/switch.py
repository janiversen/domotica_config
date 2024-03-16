"""Switch for piso and casa"""
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.core import callback
from homeassistant.const import STATE_OFF, STATE_ON

from .base import _LOGGER, CONF_CASA, CalcSwitch


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.debug('setup piso_casa switch platform')
    casa = discovery_info[CONF_CASA]
    switches = [
        CalcSwitch(hass, "vamos_a_estar", SwitchDeviceClass.SWITCH)
    ]
    if casa:
        switches.extend([])
    else:
        switches.extend([piso_led(hass, "salon"), piso_led(hass, "dormitorio")])
    if switches:
        async_add_entities(switches, True)


class piso_led(CalcSwitch):
    """Control LED dormitorio/salon."""

    def __init__(self, hass, where):
        """Setup class."""
        self.rgb_name = f"light.{where}_rgb_channel_1"
        self.rest_name = f"rest_command.{where}_rgb_rest"
        super().__init__(hass, f"{where}_rgb_rest", SwitchDeviceClass.SWITCH)
        async_track_state_change_event(
            self.hass, [self.rgb_name], self.async_onoff
        )
        self._attr_available = True
        self._attr_is_on = (self.hass.states.get(self.rgb_name).state == STATE_ON)


    @callback
    def async_onoff(self, event) -> None:
        """Track production."""
        self._attr_available = True
        self._attr_is_on = (event.data["new_state"].state == STATE_ON)
        _LOGGER.debug(f'piso_casa tracker {self._attr_unique_id} got {self._attr_is_on}')
        self.async_write_ha_state()

    async def async_turn_on(self) -> None:
        """Turn switch on."""
        _LOGGER.debug(f'piso_casa {self._attr_unique_id} turn X on')
        # self._attr_available = True
        # self._attr_is_on = True
        # self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn switch off."""
        _LOGGER.debug(f'piso_casa {self._attr_unique_id} turn X off')
        # self._attr_available = True
        # self._attr_is_on = False
        # self.async_write_ha_state()

    async def async_toggle(self) -> None:
        """Toggle switch."""
        _LOGGER.debug(f'piso_casa {self._attr_unique_id} toggle X {self._attr_is_on}')
        # self._attr_available = True
        # if not self._attr_is_on:
        #     self._attr_is_on = True
        # else:
        #     self._attr_is_on = not self._attr_is_on
        # self.async_write_ha_state()
