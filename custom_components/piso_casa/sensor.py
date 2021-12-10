""" Calculated sensors for piso and casa"""

from .base import _LOGGER, CONF_CASA, CalcSensor


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.debug('setup piso_casa sensor platform')
    casa = discovery_info[CONF_CASA]
    sensors = []
    if casa:
        sensors.extend([
            CalcSensor("casa_consumo", "energy", "Wh"),
        ])
    else:
        sensors.extend([])
    if sensors:
        async_add_entities(sensors, True)
