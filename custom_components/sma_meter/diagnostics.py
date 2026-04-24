"""Diagnostics support for Smart Meter Adapter (SMA)."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_HOST, OBIS_DESCRIPTION_MAP
from .coordinator import SmaDataCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: SmaDataCoordinator = entry.runtime_data
    available = coordinator.client.available_obis
    all_known = set(OBIS_DESCRIPTION_MAP.keys())

    return {
        "config": {
            "host": entry.data.get(CONF_HOST, "unknown"),
            "scan_interval": coordinator.update_interval.total_seconds()
            if coordinator.update_interval
            else None,
        },
        "last_update_success": coordinator.last_update_success,
        "obis_codes": {
            "total_known": len(all_known),
            "available": sorted(available),
            "unavailable": sorted(all_known - available),
        },
        "data": coordinator.data if coordinator.data else {},
        "device_info": coordinator.device_info_data,
    }
