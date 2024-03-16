"""Switch for piso and casa"""
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.helpers.event import async_track_state_change_event

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
        self.my_name = where + "_rgb"
        self.rest_name = self.my_name + "_rest"
        super().__init__(hass, self.rest_name, SwitchDeviceClass.SWITCH)
        # async_track_state_change_event(
        #     self.hass, ["sensor.production"], self.async_track_production
        # )
        # async_track_state_change_event(
        #     self.hass, ["sensor.power_meter"], self.async_track_power_meter
        # )
