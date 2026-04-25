"""Smart Meter Adapter (SMA) HTTP API client."""

from __future__ import annotations

import logging
import ssl
from typing import Any

import aiohttp

from .const import (
    API_ENDPOINT_MEASUREMENT,
    API_ENDPOINT_STATUS,
    TIMEOUT_READ,
)

_LOGGER = logging.getLogger(__name__)


class SmaApiError(Exception):
    """Error communicating with Smart Meter Adapter."""


class SmaApiClient:
    """Client for the SMA JSON API."""

    def __init__(
        self,
        host: str,
        token: str,
        session: aiohttp.ClientSession,
        *,
        use_https: bool = True,
        verify_ssl: bool = False,
    ) -> None:
        self._host = host
        self._token = token
        self._session = session
        self._use_https = use_https
        self._verify_ssl = verify_ssl
        self._available_obis: set[str] | None = None
        self._ssl_context: ssl.SSLContext | None = None

        proto = "https" if use_https else "http"
        self._base_url = f"{proto}://{host}"

        if not verify_ssl and use_https:
            self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE

    @property
    def host(self) -> str:
        return self._host

    @property
    def available_obis(self) -> set[str]:
        """Return the set of OBIS codes available on this device."""
        return self._available_obis or set()

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"TOKEN {self._token}"}

    async def async_validate_connection(self) -> bool:
        """Validate we can connect to the SMA."""
        try:
            data = await self._async_get_json(API_ENDPOINT_MEASUREMENT)
            return isinstance(data, dict) and len(data) > 0
        except SmaApiError:
            return False

    async def async_probe_available_obis(self) -> set[str]:
        """Probe which OBIS codes are present in the measurement data."""
        if self._available_obis is not None:
            return self._available_obis

        try:
            data = await self._async_get_json(API_ENDPOINT_MEASUREMENT)
        except SmaApiError:
            self._available_obis = set()
            return self._available_obis

        available: set[str] = set()
        if isinstance(data, dict):
            for key, value in data.items():
                if (
                    isinstance(value, dict)
                    and "value" in value
                    or key in ("api_version", "sma_time")
                ):
                    available.add(key)

        self._available_obis = available
        _LOGGER.debug("Probed %d available OBIS codes", len(available))
        return available

    async def async_read_measurement(self) -> dict[str, Any]:
        """Read measurement data from the SMA."""
        data = await self._async_get_json(API_ENDPOINT_MEASUREMENT)
        if isinstance(data, dict):
            return data
        return {}

    async def async_read_status(self) -> dict[str, str]:
        """Read status info (firmware, serial, etc.).

        Errors are silently suppressed so setup does not fail
        when the status endpoint is unavailable.
        """
        result: dict[str, str] = {}
        try:
            data = await self._async_get_json(API_ENDPOINT_STATUS)
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (str, int, float)):
                        result[key] = str(value)
                    elif isinstance(value, dict):
                        # Flatten nested dicts with dot notation
                        for sub_key, sub_value in value.items():
                            if isinstance(sub_value, (str, int, float)):
                                result[f"{key}.{sub_key}"] = str(sub_value)
        except SmaApiError:
            _LOGGER.debug("Status endpoint not available")
        return result

    async def _async_get_json(self, endpoint: str) -> Any:
        """Perform a GET request and return the JSON response."""
        url = f"{self._base_url}{endpoint}"
        kwargs: dict[str, Any] = {
            "headers": self._headers(),
            "timeout": aiohttp.ClientTimeout(total=TIMEOUT_READ),
        }
        if self._ssl_context is not None:
            kwargs["ssl"] = self._ssl_context

        try:
            async with self._session.get(url, **kwargs) as resp:
                if resp.status != 200:
                    raise SmaApiError(f"HTTP {resp.status} from {endpoint}")
                return await resp.json()
        except aiohttp.ClientError as err:
            raise SmaApiError(f"Connection error: {err}") from err
        except TimeoutError as err:
            raise SmaApiError(f"Timeout connecting to {self._host}") from err
