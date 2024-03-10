"""Calculated sensors for piso and casa"""
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfPower
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_state_change_event

from .base import _LOGGER, CONF_CASA, CalcSensor


async def async_setup_platform(
    hass,
    config,
    async_add_entities,
    discovery_info=None
):
    _LOGGER.debug('setup piso_casa sensor platform')
    casa = discovery_info[CONF_CASA]
    sensors = []
    if casa:
        sensors.extend([
            CasaConsumo(hass),
        ])
    else:
        sensors.extend([])
    if sensors:
        async_add_entities(sensors, True)


class CasaConsumo(CalcSensor):
    """Class to show consumption local."""

    production: int = 0
    power_meter: int = 0

    def __init__(self, hass):
        """Setup class."""
        super().__init__(hass, "casa_consumo", SensorDeviceClass.POWER, UnitOfPower.WATT)
        async_track_state_change_event(
            self.hass, ["sensor.production"], self.async_track_production
        )
        async_track_state_change_event(
            self.hass, ["sensor.power_meter"], self.async_track_power_meter
        )

    @callback
    def async_track_production(self, event) -> None:
        """Track production."""
        try:
            self.production = int(event.data["new_state"].state)
        except ValueError:
            return
        self._attr_native_value = self.production - self.power_meter
        self.async_write_ha_state()

    @callback
    def async_track_power_meter(self, event) -> None:
        """Track production."""
        try:
            self.power_meter = int(event.data["new_state"].state)
        except ValueError:
            return
        self._attr_native_value = self.production - self.power_meter
        self.async_write_ha_state()
