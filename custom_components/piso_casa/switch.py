""" Switch for piso and casa"""

from .base import _LOGGER, CONF_CASA, CalcSwitch

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.debug('setup piso_casa switch platform')
    casa = discovery_info[CONF_CASA]
    switches = [
        CalcSwitch("vamos_a_estar", None, "")
    ]
    if casa:
        switches.extend([])
    else:
        switches.extend([])
    if switches:
        async_add_entities(switches, True)
