""" piso and casa base."""
import logging

from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.components.sensor import RestoreSensor, SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON, STATE_OFF

DOMAIN = "piso_casa"
CONF_CASA = "casa"

_LOGGER = logging.getLogger(f"custom_components.{DOMAIN}")


class Base:
    """Class for all entities."""

    def __init__(
        self,
        name: str,
        device_class: str,
        measurement_unit: str,
        ) -> None:
        """Initialize entity."""
        self._attr_available = True
        self._attr_should_poll = False
        self._attr_is_on = None
        self._attr_value = None
        self._attr_state_class = None

        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}.{name}"
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = measurement_unit
        _LOGGER.info(f'Calculated {self._attr_name} created')


class CalcSensor(Base, RestoreSensor, SensorEntity):
    """Class for all entities."""

    def __init__(
        self,
        name: str,
        device_class: str,
        measurement_unit: str,
        ) -> None:
        """Initialize entity."""
        super().__init__(name, device_class, measurement_unit)

    async def async_added_to_hass(self) -> None:
        """Notify entity added to hass."""
        _LOGGER.debug(f'piso_casa {self._attr_unique_id} added to hass')
        await super().async_added_to_hass()
        if state := await self.async_get_last_sensor_data():
            self._attr_native_value = state.native_value

    async def set(self, value):
        _LOGGER.debug(f'piso_casa {self._attr_unique_id} set value {value}')
        self._attr_native_value = value
        await self.async_schedule_update_ha_state()


class CalcSwitch(Base, RestoreEntity, SwitchEntity):
    """Class for all entities."""

    def __init__(
        self,
        name: str,
        device_class: str,
        measurement_unit: str,
        ) -> None:
        """Initialize entity."""
        super().__init__(name, device_class, measurement_unit)

    async def async_added_to_hass(self) -> None:
        """Notify entity added to hass."""
        _LOGGER.debug(f'piso_casa {self._attr_unique_id} added to hass')
        await super().async_added_to_hass()
        if state := await self.async_get_last_state():
            if state.state == STATE_ON:
                self._attr_is_on = True
            elif state.state == STATE_OFF:
                self._attr_is_on = False

    async def async_turn_on(self) -> None:
        """Turn switch on."""
        _LOGGER.debug(f'piso_casa {self._attr_unique_id} turn on')
        self._attr_available = True
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        """Turn switch off."""
        _LOGGER.debug(f'piso_casa {self._attr_unique_id} turn off')
        self._attr_available = True
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_toggle(self) -> None:
        """Toggle switch."""
        _LOGGER.debug(f'piso_casa {self._attr_unique_id} toggle {self._attr_is_on}')
        self._attr_available = True
        if not self._attr_is_on:
            self._attr_is_on = True
        else:
            self._attr_is_on = not self._attr_is_on
        self.async_write_ha_state()
