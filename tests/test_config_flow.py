"""Tests for SMA config flow."""

from __future__ import annotations

from unittest.mock import patch

import voluptuous as vol
from homeassistant.config_entries import SOURCE_RECONFIGURE, SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.sma_meter.const import (
    CONF_HOST,
    CONF_SCAN_INTERVAL,
    CONF_TOKEN,
    CONF_USE_HTTPS,
    CONF_VERIFY_SSL,
    DEFAULT_HOST,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_USE_HTTPS,
    DEFAULT_VERIFY_SSL,
    DOMAIN,
)


async def test_config_flow_init(hass: HomeAssistant) -> None:
    """Test the initial form is shown."""
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_USER})

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}


async def test_config_flow_success(hass: HomeAssistant) -> None:
    """Test successful config flow."""
    with (
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_validate_connection",
            return_value=True,
        ),
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_read_device_id",
            return_value="SMA-DEVICE-001",
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
            return_value={"1-0:1.8.0": 105.119},
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data={
                CONF_HOST: "192.168.1.100",
                CONF_TOKEN: "secret",
                CONF_USE_HTTPS: True,
                CONF_VERIFY_SSL: False,
                CONF_SCAN_INTERVAL: 30,
            },
        )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "SMA (192.168.1.100)"
    assert result["data"][CONF_HOST] == "192.168.1.100"
    assert result["data"][CONF_TOKEN] == "secret"


async def test_config_flow_cannot_connect(hass: HomeAssistant) -> None:
    """Test config flow with connection error."""
    with patch(
        "custom_components.sma_meter.config_flow.SmaApiClient.async_validate_connection",
        return_value=False,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data={
                CONF_HOST: "192.168.1.100",
                CONF_TOKEN: "secret",
                CONF_USE_HTTPS: True,
                CONF_VERIFY_SSL: False,
                CONF_SCAN_INTERVAL: 30,
            },
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"]["base"] == "cannot_connect"


async def test_config_flow_duplicate(hass: HomeAssistant) -> None:
    """Test config flow with duplicate entry."""
    with (
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_validate_connection",
            return_value=True,
        ),
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_read_device_id",
            return_value="SMA-DEVICE-001",
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
            return_value={"1-0:1.8.0": 105.119},
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data={
                CONF_HOST: "192.168.1.100",
                CONF_TOKEN: "secret",
                CONF_USE_HTTPS: True,
                CONF_VERIFY_SSL: False,
                CONF_SCAN_INTERVAL: 30,
            },
        )
    assert result["type"] == FlowResultType.CREATE_ENTRY

    # Try duplicate
    with (
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_validate_connection",
            return_value=True,
        ),
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_read_device_id",
            return_value="SMA-DEVICE-001",
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data={
                CONF_HOST: "192.168.1.100",
                CONF_TOKEN: "secret",
                CONF_USE_HTTPS: True,
                CONF_VERIFY_SSL: False,
                CONF_SCAN_INTERVAL: 30,
            },
        )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_options_flow(hass: HomeAssistant) -> None:
    """Test options flow."""
    with (
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_validate_connection",
            return_value=True,
        ),
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_read_device_id",
            return_value="SMA-DEVICE-001",
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
            return_value={"1-0:1.8.0": 105.119},
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data={
                CONF_HOST: "192.168.1.100",
                CONF_TOKEN: "secret",
                CONF_SCAN_INTERVAL: 30,
            },
        )

        assert result["type"] == FlowResultType.CREATE_ENTRY
        entry = result["result"]

        result = await hass.config_entries.options.async_init(entry.entry_id)

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "init"

        result = await hass.config_entries.options.async_configure(
            result["flow_id"],
            user_input={CONF_SCAN_INTERVAL: 60},
        )

        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert result["data"][CONF_SCAN_INTERVAL] == 60


async def test_reconfigure_flow(hass: HomeAssistant) -> None:
    """Test reconfigure flow for changing host."""
    with (
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_validate_connection",
            return_value=True,
        ),
        patch(
            "custom_components.sma_meter.config_flow.SmaApiClient.async_read_device_id",
            return_value="SMA-DEVICE-001",
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
            return_value={"1-0:1.8.0": 105.119},
        ),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data={
                CONF_HOST: "192.168.1.100",
                CONF_TOKEN: "secret",
                CONF_SCAN_INTERVAL: 30,
            },
        )

        assert result["type"] == FlowResultType.CREATE_ENTRY
        entry = result["result"]

        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={
                "source": SOURCE_RECONFIGURE,
                "entry_id": entry.entry_id,
            },
        )

        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "reconfigure"

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_HOST: "192.168.1.200",
                CONF_TOKEN: "new-secret",
                CONF_USE_HTTPS: False,
                CONF_VERIFY_SSL: False,
            },
        )

        assert result["type"] == FlowResultType.ABORT
        assert result["reason"] == "reconfigure_successful"


async def test_default_values_in_form(hass: HomeAssistant) -> None:
    """Test that default values are shown in the form."""
    from custom_components.sma_meter.config_flow import DATA_SCHEMA

    defaults = {}
    for key in DATA_SCHEMA.schema:
        if hasattr(key, "default") and key.default is not vol.UNDEFINED:
            defaults[str(key)] = key.default() if callable(key.default) else key.default

    assert defaults[CONF_HOST] == DEFAULT_HOST
    assert defaults[CONF_USE_HTTPS] == DEFAULT_USE_HTTPS
    assert defaults[CONF_VERIFY_SSL] == DEFAULT_VERIFY_SSL
    assert defaults[CONF_SCAN_INTERVAL] == DEFAULT_SCAN_INTERVAL
