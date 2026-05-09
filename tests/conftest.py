"""Test fixtures for Smart Meter Adapter (SMA) integration."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

import pytest
from aioresponses import aioresponses
from homeassistant.core import HomeAssistant


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest."""
    config.addinivalue_line("markers", "asyncio: mark test as async")


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> Generator[None]:
    """Enable custom integrations in Home Assistant."""
    yield


@pytest.fixture
async def hass(hass: HomeAssistant) -> HomeAssistant:
    """Return a Home Assistant instance."""
    return hass


@pytest.fixture
def mock_api() -> Generator[aioresponses]:
    """Create a mock SMA API using aioresponses."""
    with aioresponses() as m:
        yield m


@pytest.fixture
def measurement_data() -> dict[str, Any]:
    """Return sample measurement data."""
    return {
        "1-0:1.8.0": {"value": 105119, "time": 1104625548},
        "1-0:2.8.0": {"value": 0, "time": 1104625548},
        "1-0:1.7.0": {"value": 33, "time": 1104625548},
        "1-0:2.7.0": {"value": 0, "time": 1104625548},
        "1-0:16.7.0": {"value": 33, "time": 1104625548},
        "api_version": "v1",
        "name": "SMA-DEVICE-001",
        "sma_time": 14011.8,
    }


@pytest.fixture
def status_data() -> dict[str, Any]:
    """Return sample status data."""
    return {
        "name": "SMA-DEVICE-001",
        "fw_version": "1.2.3",
        "meter": {
            "manufacturer": "NES",
            "name": "METER-TEST-001",
        },
    }
