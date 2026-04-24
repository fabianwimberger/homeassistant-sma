# Smart Meter Adapter (SMA) for Home Assistant

[![CI](https://github.com/fabianwimberger/homeassistant-sma/actions/workflows/ci.yml/badge.svg)](https://github.com/fabianwimberger/homeassistant-sma/actions)
[![codecov](https://codecov.io/gh/fabianwimberger/homeassistant-sma/branch/main/graph/badge.svg)](https://codecov.io/gh/fabianwimberger/homeassistant-sma)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **⚠️ Disclaimer**: This is an independent, open-source project created by the community. It is **not affiliated with, endorsed by, or sponsored by Österreichs E-Wirtschaft**. Use at your own risk.

Custom integration for [Home Assistant](https://www.home-assistant.io/) that communicates directly with the **Smart Meter Adapter (SMA)** via its built-in JSON REST API. No MQTT broker or middleman needed.

## Background

The Smart Meter Adapter (SMA) from Österreichs E-Wirtschaft reads encrypted smart meter data locally and exposes it via a JSON REST API. There is no native Home Assistant integration for it. This integration polls the SMA directly, auto-discovers which OBIS codes your meter supports, and exposes them as HA sensors with correct units and scaling.

## Features

- **Auto-discovery** — probes available OBIS codes at startup (meters vary by configuration)
- **Correct scaling** — Wh → kWh for energy values automatically
- **Per-phase sensors** — power, current, and voltage for L1–L3
- **Device info** — firmware version and SMA ID read from hardware
- **Diagnostics** — built-in HA diagnostics export for troubleshooting
- **Configurable polling** — scan interval from 5 to 300 seconds
- **Re-configurable** — change host or token without re-adding the integration

## Quick Start

### Installation (HACS - Recommended)

1. Open HACS in Home Assistant
2. Click the three dots in the top right and select **Custom repositories**
3. Add `https://github.com/fabianwimberger/homeassistant-sma` as an **Integration**
4. Search for "Smart Meter Adapter (SMA)" and install it
5. Restart Home Assistant

### Installation (Manual)

```bash
# Clone into your Home Assistant custom_components directory
cd /path/to/homeassistant/config
git clone https://github.com/fabianwimberger/homeassistant-sma.git
mv homeassistant-sma/custom_components/sma_meter custom_components/
rm -rf homeassistant-sma
```

Restart Home Assistant.

### Configuration

1. Go to **Settings > Devices & Services > Add Integration**
2. Search for "Smart Meter Adapter (SMA)"
3. Enter the IP address of your SMA (e.g. `192.168.1.100`)
4. Enter the **Authorization Token** from the SMA web UI under *API → JSON*
5. Configure HTTPS and SSL verification as needed
6. Set the scan interval in seconds (default: 15, range: 5-300)

The integration validates the connection by reading the device status before completing setup.

## How It Works

```
Startup → Probe available OBIS codes → Read device info → Create sensors → Poll for updates
```

The SMA API returns a JSON object with all available OBIS codes. At startup, the integration probes each code to determine which sensors to create. This handles different meter configurations without manual configuration.

## Supported Sensors

The integration creates sensors only for OBIS codes that your meter actually provides.
Common sensors include:

| Sensor | OBIS | Unit |
|---|---|---|
| Active energy import total | 1-0:1.8.0 | kWh |
| Active energy export total | 1-0:2.8.0 | kWh |
| Active power import | 1-0:1.7.0 | W |
| Active power export | 1-0:2.7.0 | W |
| Active power sum | 1-0:16.7.0 | W |
| Active power L1–L3 | 1-0:21/41/61.7.0 | W |
| Current L1–L3 | 1-0:31/51/71.7.0 | A |
| Voltage L1–L3 | 1-0:32/52/72.7.0 | V |
| Frequency | 1-0:14.7.0 | Hz |
| Power factor | 1-0:13.7.0 | – |

## Diagnostics

The integration supports Home Assistant's built-in diagnostics export. Go to the integration page and click **Download diagnostics** to get a JSON dump of the current configuration and sensor values.

## Configuration

### Changing Settings After Setup

- **Host / Token**: Use the "Reconfigure" option on the integration card to change connection settings
- **Scan interval**: Use the "Configure" option to adjust the polling interval at runtime

## Troubleshooting

**No sensors appearing:**
- Verify the SMA IP address is correct
- Check that the SMA web interface is accessible
- Ensure the authorization token is valid
- Download diagnostics to see which OBIS codes were probed

**Sensors showing as unavailable:**
- Check network connectivity to the SMA
- Some OBIS codes may not be available on your specific meter configuration

## Development

```bash
pip install -e ".[dev]"
pytest
```

See [docs/TESTING.md](docs/TESTING.md) for testing with a fresh Home Assistant instance.

## License & Disclaimer

MIT License — see [LICENSE](LICENSE) file.

This project uses the "Smart Meter Adapter (SMA)" name to identify the compatible device. This project is an independent, community-created integration and is **not affiliated with, endorsed by, or sponsored by Österreichs E-Wirtschaft**. Use of the SMA name is for identification and compatibility purposes only.
