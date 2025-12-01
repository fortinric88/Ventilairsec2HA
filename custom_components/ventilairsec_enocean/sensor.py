from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Expose a generic sensor that reflects a lot of values.
    async_add_entities([VentilairsecGenericSensor(coordinator, "ventilairsec_status")])


class VentilairsecGenericSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, name: str) -> None:
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"ventilairsec_{name}"

    @property
    def state(self):
        # Return a summary state when available
        data = self.coordinator.data
        if not data:
            return None
        # try to return a primary field if available
        for key in ("filter", "mode", "IDMACH::value"):
            if key in data:
                return data.get(key)
        return "connected"

    @property
    def extra_state_attributes(self):
        return self.coordinator.data
