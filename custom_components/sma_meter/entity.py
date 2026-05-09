"""Base entity for Smart Meter Adapter (SMA)."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SmaDataCoordinator


class SmaEntity(CoordinatorEntity[SmaDataCoordinator]):
    """Base entity for SMA."""

    _attr_has_entity_name = True
    _sma_key: str = ""

    def __init__(self, coordinator: SmaDataCoordinator) -> None:
        super().__init__(coordinator)
        info = coordinator.device_info_data
        device_id = info.get("device_id") or coordinator.client.host
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=info.get("name", "Smart Meter Adapter"),
            manufacturer=info.get("manufacturer", "Smart Meter Adapter"),
            model="Smart Meter Adapter",
            sw_version=info.get("firmware_version"),
            serial_number=info.get("serial_number"),
        )

    @property
    def available(self) -> bool:
        """Return True if the entity's key is present in coordinator data."""
        if not super().available:
            return False
        if self.coordinator.data is None:
            return False
        if self._sma_key:
            return self._sma_key in self.coordinator.data
        return True
