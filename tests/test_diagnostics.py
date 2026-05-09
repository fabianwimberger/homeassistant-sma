"""Tests for SMA diagnostics."""

from __future__ import annotations

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.sma_meter.diagnostics import async_get_config_entry_diagnostics


async def test_diagnostics(hass: HomeAssistant) -> None:
    """Test diagnostics output."""
    entry = MagicMock()
    entry.data = {"host": "192.168.1.100", "token": "secret-token"}

    coordinator = MagicMock()
    coordinator.client.available_obis = {"1-0:1.8.0", "1-0:1.7.0"}
    coordinator.last_update_success = True
    coordinator.update_interval.total_seconds.return_value = 30
    coordinator.data = {"1-0:1.8.0": 105.0, "1-0:1.7.0": 33.0}
    coordinator.device_info_data = {"sma_id": "SMA-TEST"}

    entry.runtime_data = coordinator

    result = await async_get_config_entry_diagnostics(hass, entry)

    assert result["config"]["host"] == "192.168.1.100"
    assert result["config"]["entry_data"]["token"] == "**REDACTED**"
    assert result["last_update_success"] is True
    assert result["obis_codes"]["total_known"] > 0
    assert "1-0:1.8.0" in result["obis_codes"]["available"]
    assert result["data"]["1-0:1.8.0"] == 105.0
    assert result["device_info"]["sma_id"] == "SMA-TEST"
