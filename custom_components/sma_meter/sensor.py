"""Sensor platform for Smart Meter Adapter (SMA)."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    SENSOR_DESCRIPTIONS,
    SmaSensorEntityDescription,
)
from .coordinator import SmaDataCoordinator
from .entity import SmaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SMA sensors."""
    coordinator: SmaDataCoordinator = entry.runtime_data
    available = coordinator.client.available_obis

    entities: list[SmaSensor] = []
    for desc in SENSOR_DESCRIPTIONS:
        if desc.obis_code in available:
            entities.append(SmaSensor(coordinator, desc))

    async_add_entities(entities)


class SmaSensor(SmaEntity, SensorEntity):
    """SMA sensor entity."""

    entity_description: SmaSensorEntityDescription

    def __init__(
        self,
        coordinator: SmaDataCoordinator,
        description: SmaSensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._sma_key = description.obis_code
        self._attr_unique_id = f"{coordinator.client.host}_{description.key}"

    @property
    def native_value(self) -> float | int | str | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        raw: float | str | None = self.coordinator.data.get(self._sma_key)
        if raw is None:
            return None

        if isinstance(raw, str):
            return raw

        scaled = raw * self.entity_description.scale

        # Return as int when the scaled value is a whole number and the
        # original description does not imply fractional values (energy,
        # power, current, voltage are typically fine as float).
        if scaled == int(scaled) and self.entity_description.scale != 1.0:
            return int(scaled)

        return round(scaled, 3)
