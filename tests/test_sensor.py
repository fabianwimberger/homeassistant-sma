"""Tests for SMA sensor platform."""

from __future__ import annotations

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.sma_meter.const import OBIS_DESCRIPTION_MAP
from custom_components.sma_meter.sensor import SmaSensor


async def test_sensor_native_value(hass: HomeAssistant) -> None:
    """Test sensor native value with scaling."""
    coordinator = MagicMock()
    coordinator.client = MagicMock()
    coordinator.client.host = "192.168.1.100"
    coordinator.data = {"1-0:1.8.0": 105119}
    coordinator.device_info_data = {}

    desc = OBIS_DESCRIPTION_MAP["1-0:1.8.0"]
    sensor = SmaSensor(coordinator, desc)
    assert sensor.native_value == 105.119  # 105119 * 0.001

    coordinator.data = {"1-0:1.8.0": 105000}
    assert sensor.native_value == 105  # whole number -> int

    coordinator.data = {"1-0:1.8.0": 105119.5}
    assert sensor.native_value == 105.12  # rounded to 3 decimals


async def test_sensor_power_no_scaling(hass: HomeAssistant) -> None:
    """Test power sensor has no scaling applied."""
    coordinator = MagicMock()
    coordinator.client = MagicMock()
    coordinator.client.host = "192.168.1.100"
    coordinator.data = {"1-0:1.7.0": 33}
    coordinator.device_info_data = {}

    desc = OBIS_DESCRIPTION_MAP["1-0:1.7.0"]
    sensor = SmaSensor(coordinator, desc)
    assert sensor.native_value == 33


async def test_sensor_unique_id(hass: HomeAssistant) -> None:
    """Test sensor unique ID."""
    coordinator = MagicMock()
    coordinator.client = MagicMock()
    coordinator.client.host = "192.168.1.100"
    coordinator.data = {}
    coordinator.device_info_data = {}

    desc = OBIS_DESCRIPTION_MAP["1-0:1.8.0"]
    sensor = SmaSensor(coordinator, desc)
    assert sensor.unique_id == "192.168.1.100_active_energy_import_total"
