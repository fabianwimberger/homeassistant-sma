"""Tests for SMA API client."""

from __future__ import annotations

import aiohttp
import pytest
from aioresponses import aioresponses

from custom_components.sma_meter.api import SmaApiClient, SmaApiError

HOST = "192.168.1.100"
TOKEN = "test-token"


@pytest.fixture
def client(
    aiohttp_client_session: aiohttp.ClientSession,
) -> SmaApiClient:
    """Return an SMA API client."""
    return SmaApiClient(HOST, TOKEN, aiohttp_client_session)


@pytest.fixture
async def aiohttp_client_session() -> aiohttp.ClientSession:
    """Return an aiohttp ClientSession."""
    async with aiohttp.ClientSession() as session:
        yield session


async def test_validate_connection_success(mock_api: aioresponses) -> None:
    """Test successful connection validation."""
    mock_api.get(
        f"https://{HOST}/api/data/measurement.json",
        payload={"1-0:1.8.0": {"value": 100}},
        headers={"AuthorizationToken": TOKEN},
    )

    async with aiohttp.ClientSession() as session:
        client = SmaApiClient(HOST, TOKEN, session)
        assert await client.async_validate_connection() is True


async def test_validate_connection_failure(mock_api: aioresponses) -> None:
    """Test connection validation with HTTP error."""
    mock_api.get(
        f"https://{HOST}/api/data/measurement.json",
        status=401,
    )

    async with aiohttp.ClientSession() as session:
        client = SmaApiClient(HOST, TOKEN, session)
        assert await client.async_validate_connection() is False


async def test_probe_available_obis(mock_api: aioresponses, measurement_data: dict) -> None:
    """Test probing available OBIS codes."""
    mock_api.get(
        f"https://{HOST}/api/data/measurement.json",
        payload=measurement_data,
    )

    async with aiohttp.ClientSession() as session:
        client = SmaApiClient(HOST, TOKEN, session)
        available = await client.async_probe_available_obis()
        assert "1-0:1.8.0" in available
        assert "1-0:1.7.0" in available
        assert "api_version" in available
        assert "sma_time" in available


async def test_read_status(mock_api: aioresponses, status_data: dict) -> None:
    """Test reading status info."""
    mock_api.get(
        f"https://{HOST}/api/sma/status.json",
        payload=status_data,
    )

    async with aiohttp.ClientSession() as session:
        client = SmaApiClient(HOST, TOKEN, session)
        result = await client.async_read_status()
        assert result["sma_id"] == "SMA-12345"
        assert result["firmware_version"] == "1.2.3"


async def test_read_status_suppressed_error(mock_api: aioresponses) -> None:
    """Test that status read errors are suppressed."""
    mock_api.get(
        f"https://{HOST}/api/sma/status.json",
        status=500,
    )

    async with aiohttp.ClientSession() as session:
        client = SmaApiClient(HOST, TOKEN, session)
        result = await client.async_read_status()
        assert result == {}


async def test_http_error_raises(mock_api: aioresponses) -> None:
    """Test that HTTP errors raise SmaApiError."""
    mock_api.get(
        f"https://{HOST}/api/data/measurement.json",
        status=500,
    )

    async with aiohttp.ClientSession() as session:
        client = SmaApiClient(HOST, TOKEN, session)
        with pytest.raises(SmaApiError):
            await client.async_read_measurement()
