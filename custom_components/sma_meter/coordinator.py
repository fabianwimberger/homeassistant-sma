"""Data update coordinator for Smart Meter Adapter (SMA)."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SmaApiClient, SmaApiError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SmaDataCoordinator(DataUpdateCoordinator[dict[str, float | str]]):
    """Coordinator to manage fetching SMA data."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: SmaApiClient,
        scan_interval: int,
        device_info: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.client = client
        self.device_info_data = device_info or {}

    async def _async_update_data(self) -> dict[str, float | str]:
        """Fetch data from the SMA."""
        try:
            raw = await self.client.async_read_measurement()
        except SmaApiError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

        result: dict[str, float | str] = {}
        if not isinstance(raw, dict):
            return result

        for key, value in raw.items():
            if isinstance(value, dict) and "value" in value:
                parsed = _parse_value(value["value"])
                if parsed is not None:
                    result[key] = parsed
            elif key == "api_version" and isinstance(value, str):
                result[key] = value
            elif key == "sma_time":
                parsed = _parse_value(value)
                if parsed is not None:
                    result[key] = parsed

        return result


def _parse_value(value: object) -> float | None:
    """Parse a raw value to float."""
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        if value == "true":
            return 1.0
        if value == "false":
            return 0.0
        try:
            return float(value)
        except ValueError:
            return None
    return None
