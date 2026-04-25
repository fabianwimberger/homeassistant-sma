"""Constants for the Smart Meter Adapter (SMA) integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
)

DOMAIN = "sma_meter"

CONF_HOST = "host"
CONF_TOKEN = "token"
CONF_USE_HTTPS = "use_https"
CONF_VERIFY_SSL = "verify_ssl"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_HOST = "192.168.100.1"
DEFAULT_USE_HTTPS = True
DEFAULT_VERIFY_SSL = False
DEFAULT_SCAN_INTERVAL = 30
MIN_SCAN_INTERVAL = 5
MAX_SCAN_INTERVAL = 300

API_ENDPOINT_MEASUREMENT = "/api/v1/measurement"
API_ENDPOINT_STATUS = "/api/v1/status"

TIMEOUT_DEFAULT = 10
TIMEOUT_READ = 15


@dataclass(frozen=True)
class SmaSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for SMA."""

    obis_code: str = ""
    scale: float = 1.0


# --- Known OBIS code descriptions ---
# OBIS codes vary by meter model; only codes present in the API response
# are exposed as entities. Energy values are in Wh and scaled to kWh.

SENSOR_DESCRIPTIONS: tuple[SmaSensorEntityDescription, ...] = (
    # Energy – total
    SmaSensorEntityDescription(
        key="active_energy_import_total",
        obis_code="1-0:1.8.0",
        translation_key="active_energy_import_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        scale=0.001,
    ),
    SmaSensorEntityDescription(
        key="active_energy_export_total",
        obis_code="1-0:2.8.0",
        translation_key="active_energy_export_total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        scale=0.001,
    ),
    # Energy – tariff 1
    SmaSensorEntityDescription(
        key="active_energy_import_tariff1",
        obis_code="1-0:1.8.1",
        translation_key="active_energy_import_tariff1",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        scale=0.001,
    ),
    SmaSensorEntityDescription(
        key="active_energy_export_tariff1",
        obis_code="1-0:2.8.1",
        translation_key="active_energy_export_tariff1",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        scale=0.001,
    ),
    # Energy – tariff 2
    SmaSensorEntityDescription(
        key="active_energy_import_tariff2",
        obis_code="1-0:1.8.2",
        translation_key="active_energy_import_tariff2",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        scale=0.001,
    ),
    SmaSensorEntityDescription(
        key="active_energy_export_tariff2",
        obis_code="1-0:2.8.2",
        translation_key="active_energy_export_tariff2",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        scale=0.001,
    ),
    # Power – total
    SmaSensorEntityDescription(
        key="active_power_import",
        obis_code="1-0:1.7.0",
        translation_key="active_power_import",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmaSensorEntityDescription(
        key="active_power_export",
        obis_code="1-0:2.7.0",
        translation_key="active_power_export",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmaSensorEntityDescription(
        key="active_power_sum",
        obis_code="1-0:16.7.0",
        translation_key="active_power_sum",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Power – per phase
    SmaSensorEntityDescription(
        key="active_power_l1",
        obis_code="1-0:21.7.0",
        translation_key="active_power_l1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmaSensorEntityDescription(
        key="active_power_l2",
        obis_code="1-0:41.7.0",
        translation_key="active_power_l2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmaSensorEntityDescription(
        key="active_power_l3",
        obis_code="1-0:61.7.0",
        translation_key="active_power_l3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Current
    SmaSensorEntityDescription(
        key="current_l1",
        obis_code="1-0:31.7.0",
        translation_key="current_l1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmaSensorEntityDescription(
        key="current_l2",
        obis_code="1-0:51.7.0",
        translation_key="current_l2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmaSensorEntityDescription(
        key="current_l3",
        obis_code="1-0:71.7.0",
        translation_key="current_l3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Voltage
    SmaSensorEntityDescription(
        key="voltage_l1",
        obis_code="1-0:32.7.0",
        translation_key="voltage_l1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmaSensorEntityDescription(
        key="voltage_l2",
        obis_code="1-0:52.7.0",
        translation_key="voltage_l2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SmaSensorEntityDescription(
        key="voltage_l3",
        obis_code="1-0:72.7.0",
        translation_key="voltage_l3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Frequency
    SmaSensorEntityDescription(
        key="frequency",
        obis_code="1-0:14.7.0",
        translation_key="frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Power factor
    SmaSensorEntityDescription(
        key="power_factor",
        obis_code="1-0:13.7.0",
        translation_key="power_factor",
        device_class=SensorDeviceClass.POWER_FACTOR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Reactive energy
    SmaSensorEntityDescription(
        key="reactive_energy_import",
        obis_code="1-0:3.8.0",
        translation_key="reactive_energy_import",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        scale=0.001,
    ),
    SmaSensorEntityDescription(
        key="reactive_energy_export",
        obis_code="1-0:4.8.0",
        translation_key="reactive_energy_export",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        scale=0.001,
    ),
    # Diagnostics – meta fields from measurement.json
    SmaSensorEntityDescription(
        key="api_version",
        obis_code="api_version",
        translation_key="api_version",
        entity_registry_enabled_default=False,
    ),
    SmaSensorEntityDescription(
        key="sma_time",
        obis_code="sma_time",
        translation_key="sma_time",
        entity_registry_enabled_default=False,
    ),
)

# Build lookup maps
OBIS_DESCRIPTION_MAP: dict[str, SmaSensorEntityDescription] = {
    desc.obis_code: desc for desc in SENSOR_DESCRIPTIONS
}

PLATFORMS = ["sensor"]
