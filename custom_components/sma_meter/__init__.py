"""Smart Meter Adapter (SMA) integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SmaApiClient
from .const import (
    CONF_HOST,
    CONF_SCAN_INTERVAL,
    CONF_TOKEN,
    CONF_USE_HTTPS,
    CONF_VERIFY_SSL,
    DEFAULT_SCAN_INTERVAL,
    PLATFORMS,
)
from .const import (
    DOMAIN as DOMAIN,
)
from .coordinator import SmaDataCoordinator

_LOGGER = logging.getLogger(__name__)

type SmaConfigEntry = ConfigEntry[SmaDataCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: SmaConfigEntry) -> bool:
    """Set up Smart Meter Adapter (SMA) from a config entry."""
    host = entry.data[CONF_HOST]
    token = entry.data[CONF_TOKEN]
    use_https = entry.data.get(CONF_USE_HTTPS, True)
    verify_ssl = entry.data.get(CONF_VERIFY_SSL, False)
    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )

    session = async_get_clientsession(hass)
    client = SmaApiClient(
        host,
        token,
        session,
        use_https=use_https,
        verify_ssl=verify_ssl,
    )

    # Probe which OBIS codes are available on this device
    await client.async_probe_available_obis()

    # Read device info once at setup
    status_data = await client.async_read_status()
    device_id = (
        status_data.get("name")
        or status_data.get("serial_number")
        or status_data.get("sma_id", host)
    )
    device_info = {
        "device_id": device_id,
        "name": status_data.get("name", "Smart Meter Adapter"),
        "firmware_version": status_data.get("firmware_version")
        or status_data.get("fw_version", ""),
        "manufacturer": status_data.get("meter.manufacturer", "Smart Meter Adapter"),
        "serial_number": status_data.get("serial_number", ""),
    }

    coordinator = SmaDataCoordinator(hass, client, scan_interval, device_info)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def _async_update_listener(hass: HomeAssistant, entry: SmaConfigEntry) -> None:
    """Reload the integration when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: SmaConfigEntry) -> bool:
    """Unload a config entry."""
    return bool(await hass.config_entries.async_unload_platforms(entry, PLATFORMS))
