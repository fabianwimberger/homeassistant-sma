# Testing with a Fresh Home Assistant Instance

This guide walks through setting up a clean Home Assistant instance to test the SMA integration without touching your production environment.

## Prerequisites

- Docker installed
- Your Smart Meter Adapter reachable on the local network
- This repo cloned locally

## 1. Start a Fresh Home Assistant Container

```bash
docker run -d \
  --name ha-test \
  --network host \
  -v /tmp/ha-test-config:/config \
  ghcr.io/home-assistant/home-assistant:stable
```

Using `--network host` so the container can reach the SMA on your LAN. The config lives in `/tmp/ha-test-config` and can be thrown away after testing.

## 2. Install the Integration

Copy the custom component into the container's config:

```bash
mkdir -p /tmp/ha-test-config/custom_components
cp -r custom_components/sma_meter /tmp/ha-test-config/custom_components/
```

Restart the container to pick up the new integration:

```bash
docker restart ha-test
```

## 3. Set Up the Integration

1. Open `http://localhost:8123` in your browser
2. Complete the onboarding (create a user, skip location/integrations)
3. Go to **Settings > Devices & Services > Add Integration**
4. Search for **Smart Meter Adapter (SMA)**
5. Enter your SMA's IP address (e.g. `192.168.1.100`)
6. Enter your API token (from the SMA web UI under API → JSON)
7. Configure HTTPS and SSL verification as needed

## 4. What to Verify

### Entities created

- Go to **Settings > Devices & Services > Smart Meter Adapter (SMA)** and click the device
- Check that only sensors for OBIS codes your meter provides are created
- Sensors should show live values, not "unavailable"

### Diagnostics

- Go to the integration page, click the three dots, **Download diagnostics**
- Open the JSON and check:
  - `config` contains your host and settings
  - `data` contains current sensor values
  - `device_info` shows firmware version

### Options flow

- On the integration card, click **Configure**
- Change the scan interval to 60s
- Verify the integration reloads and continues working

### Reconfigure flow

- On the integration card, click the three dots > **Reconfigure**
- Enter a different (invalid) IP, confirm you get a "cannot connect" error
- Enter the correct IP again, confirm it works

## 5. Cleanup

```bash
docker stop ha-test && docker rm ha-test
rm -rf /tmp/ha-test-config
```
