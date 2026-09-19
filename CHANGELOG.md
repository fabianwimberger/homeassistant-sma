# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.1.5] - 2026-09-19

Adds HACS and hassfest validation, fixes the HACS minimum Home Assistant version, and guards against version drift between the manifest and pyproject.

### Fixes

- Correct the minimum Home Assistant version declared for HACS, which was higher than the integration actually requires
- Sort the manifest keys so the integration passes hassfest validation

### CI

- Add hassfest and HACS validation workflows
- Pin the lint tools to the versions under test
- Drop the drifted dev extra in favour of `requirements_test.txt`
- Add a test that guards against version drift between the manifest and `pyproject.toml`

### Dependencies

- Bump ruff from 0.16.2 to 0.16.7
- Bump mypy from 2.3.0 to 2.3.1

### Documentation & Links

- [README](https://github.com/fabianwimberger/homeassistant-sma#readme)

## [v1.1.4] - 2026-08-15

Smart Meter Adapter now runs against Home Assistant 2026.8.2 and aiohttp 3.14.3, closing out the pending Dependabot security alerts on the aiohttp dependency chain.

### Dependencies

- Bump `homeassistant` test pin from 2026.7.2 to 2026.8.2, unblocking the aiohttp update
- Bump `aiohttp` from 3.14.1 to 3.14.3
- Bump `pytest-homeassistant-custom-component` to 0.13.356 to match
- Bump `ruff` from 0.15.20 to 0.16.2 and `mypy` from 2.1.0 to 2.3.0
- Bump `actions/setup-python` from 6 to 7
- Align integration version metadata with the release version

### Documentation & Links

- [README](https://github.com/fabianwimberger/homeassistant-sma#readme)

## [v1.1.3] - 2026-07-17

Smart Meter Adapter now runs against Home Assistant 2026.7.2 and aiohttp 3.14.1, closing out the pending Dependabot security alerts on the aiohttp dependency chain.

### Dependencies

- Bump `homeassistant` test pin from 2026.5.1 to 2026.7.2, unblocking the aiohttp update
- Bump `aiohttp` from 3.13.5 to 3.14.1
- Bump `pytest-homeassistant-custom-component` to 0.13.346 and `pytest-aiohttp` to 1.1.1 to match
- Replace unmaintained `aioresponses` with the maintained `aioresponses-ng` fork (same import path), since `aioresponses` is incompatible with aiohttp>=3.14
- Align integration version metadata with the release version

### Documentation & Links

- [README](https://github.com/fabianwimberger/homeassistant-sma#readme)

## [v1.1.2] - 2026-05-10

Smart Meter Adapter now includes local Home Assistant brand assets so the integration can show an icon in Home Assistant and HACS.

### Changes

- Add Home Assistant brand icon.png and logo.png assets under custom_components/sma_meter/brand
- Align integration version metadata with the release version

### Documentation & Links

- [README](https://github.com/fabianwimberger/homeassistant-sma#readme)

## [v1.1.1] - 2026-05-09

Smart Meter Adapter now keeps entities tied to the device-reported SMA identifier instead of the configured host.

### Fixes

- Use the SMA-reported `name` as the preferred config-entry, device, and sensor identifier
- Fall back to the meter id from measurement data when status data does not include a device name
- Read firmware version from `fw_version` in current SMA status responses
- Redact the stored token from diagnostics output
- Retry OBIS probing after temporary API failures instead of caching an empty result
- Correct the documented default scan interval

### Documentation & Links

- [README](https://github.com/fabianwimberger/homeassistant-sma#readme)

## [v1.1.0] - 2026-05-09

Robustness improvements for SMA inverter response parsing.

### Fixes
- Catch JSON decode errors in SMA response parsing instead of crashing
- Clarify operator precedence with explicit grouping
- Remove dead code

### Documentation & Links
- https://github.com/fabianwimberger/homeassistant-sma

## [v1.0.1] - 2026-05-08

Broadens the trademark disclaimer, removes third-party brand assets, and pins test dependencies to versions compatible with the Home Assistant test framework.

### Fixes

- Pin pytest, pytest-cov, and aiohttp to versions compatible with the HA test framework
- Pin test dependencies to exact versions in ``requirements_test.txt``

### Documentation

- Broaden trademark disclaimer to name Österreichs Energie

### Chores

- Removed third-party brand assets

### Dependencies

- Bump pytest from 9.0.0 to 9.0.3
- Bump pytest-cov from 7.0.0 to 7.1.0
- Bump aiohttp from 3.13.3 to 3.13.5

### Documentation & Links

- [README](https://github.com/fabianwimberger/homeassistant-sma#readme)

## [v1.0.0] - 2026-04-25

First official release. Custom Home Assistant integration that talks directly to the Austrian Smart Meter Adapter (SMA) via its local JSON REST API. No MQTT broker, no extra hardware.

#### Features

- Auto-discovery of supported OBIS codes at startup
- Correct unit scaling (Wh → kWh) for energy values
- Per-phase sensors for power, current, and voltage (L1–L3)
- Device info (firmware version, SMA ID) read from hardware
- Built-in HA diagnostics export
- Configurable polling interval (5–300 seconds)
- Re-configurable host and token without re-adding the integration

#### Installation

1. Install via HACS as a custom repository
2. Restart Home Assistant
3. Add the integration via Settings → Devices & Services

Manual install instructions are in the README.

#### Notes

- This is a community project, not affiliated with or endorsed by Österreichs E-Wirtschaft
- Requires a Smart Meter Adapter (SMA) reachable on the local network with API token enabled
