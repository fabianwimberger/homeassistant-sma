"""Tests for SMA integration setup."""

from __future__ import annotations

from unittest.mock import patch

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.sma_meter.const import (
    CONF_HOST,
    CONF_SCAN_INTERVAL,
    CONF_TOKEN,
    DOMAIN,
)


async def test_setup_entry(hass: HomeAssistant) -> None:
    """Test successful setup of a config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "192.168.1.100",
            CONF_TOKEN: "secret",
            CONF_SCAN_INTERVAL: 30,
        },
        unique_id="192.168.1.100",
    )
    entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.sma_meter.api.SmaApiClient.async_validate_connection",
            return_value=True,
        ),
        patch(
            "custom_components.sma_meter.api.SmaApiClient.async_probe_available_obis",
            return_value={"1-0:1.8.0", "1-0:1.7.0"},
        ),
        patch(
            "custom_components.sma_meter.api.SmaApiClient.async_read_status",
            return_value={"sma_id": "SMA-TEST", "firmware_version": "1.0.0"},
        ),
        patch(
            "custom_components.sma_meter.coordinator.SmaDataCoordinator._async_update_data",
            return_value={"1-0:1.8.0": 105.0, "1-0:1.7.0": 33.0},
        ),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state == ConfigEntryState.LOADED


async def test_unload_entry(hass: HomeAssistant) -> None:
    """Test unloading a config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "192.168.1.100",
            CONF_TOKEN: "secret",
            CONF_SCAN_INTERVAL: 30,
        },
        unique_id="192.168.1.100",
    )
    entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.sma_meter.api.SmaApiClient.async_validate_connection",
            return_value=True,
        ),
        patch(
            "custom_components.sma_meter.api.SmaApiClient.async_probe_available_obis",
            return_value={"1-0:1.8.0"},
        ),
        patch(
            "custom_components.sma_meter.api.SmaApiClient.async_read_status",
            return_value={},
        ),
        patch(
            "custom_components.sma_meter.coordinator.SmaDataCoordinator._async_update_data",
            return_value={"1-0:1.8.0": 105.0},
        ),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state == ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state == ConfigEntryState.NOT_LOADED
