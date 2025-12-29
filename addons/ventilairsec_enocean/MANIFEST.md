# Ventilairsec Enocean - Home Assistant Addon

## Overview

This addon provides comprehensive integration of **VMI Purevent Ventilairsec** ventilation systems with Home Assistant using the **Enocean protocol**. It enables seamless control and monitoring of your ventilation system through Home Assistant's web interface.

## Features

### Core Functionality
- 🌬️ **Full Ventilairsec Support**: Control and monitor VMI Purevent Ventilairsec systems (D1079-01-00)
- 📡 **Enocean Protocol**: Complete Enocean 4BS and 1BS packet support
- 🔌 **USB Dongle Integration**: Connect via standard USB-to-serial Enocean adapters
- 🎛️ **Fan Control**: Speed regulation and mode switching
- 📊 **Sensor Data**: Temperature, humidity, and air quality monitoring
- ⚙️ **Customizable Configuration**: Flexible serial port and baud rate settings

### Technical Features
- Multi-architecture support: amd64, armv7 (Raspberry Pi), arm64
- CRC verification for data integrity
- Asynchronous event handling
- Real-time device discovery
- Persistent logging
- Debug mode for troubleshooting

## Installation

### Prerequisites
1. Home Assistant 2023.10.0 or later
2. Enocean USB dongle (e.g., EnOcean USB 300 or compatible)
3. USB serial adapter cable (if needed)

### Setup Steps

1. **Add Repository**: Add this repository to Home Assistant's Supervisor add-on repositories:
   ```
   https://github.com/fortinric88/Ventilairsec2HA
   ```

2. **Install Addon**: Go to Settings → Add-ons → Install the Ventilairsec Enocean addon

3. **Configure Serial Port**: Update the addon configuration with your USB device:
   - `/dev/ttyUSB0` or `/dev/ttyUSB1` (for typical USB adapters)
   - `/dev/ttyACM0` or `/dev/ttyACM1` (for some Enocean dongles)

4. **Start Addon**: Enable auto-start in addon options

5. **Verify Operation**: Check addon logs for successful initialization

## Configuration

### Available Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `serial_port` | select | `/dev/ttyUSB0` | USB serial port for Enocean dongle |
| `serial_rate` | integer | 115200 | Serial communication speed (baud) |
| `socket_port` | integer | 55006 | Internal TCP communication port |
| `cycle_time` | float | 0.3 | Processing cycle time (seconds) |
| `debug_logging` | boolean | false | Enable detailed debug logging |

### Example Configuration

```yaml
serial_port: /dev/ttyUSB0
serial_rate: 115200
socket_port: 55006
cycle_time: 0.3
debug_logging: false
```

## Supported Devices

### Primary Device
- **VMI Purevent Ventilairsec** (Enocean ID: D1079-01-00)
  - Temperature and humidity sensors
  - Fan speed control
  - Ventilation modes
  - System status

### Compatible Sensors
- **A5-20-01**: Temperature and humidity sensors
- **D5-00-01**: Contact/binary status sensors

## Usage

### Accessing Device Data

Devices appear automatically in Home Assistant as:
- Temperature sensors
- Humidity sensors
- Fan entities (with speed control)
- Switch entities (for mode control)
- Binary sensors (for status)

### Automation Examples

```yaml
# Increase ventilation when humidity is high
automation:
  - trigger:
      platform: numeric_state
      entity_id: sensor.ventilairsec_humidity
      above: 60
    action:
      service: fan.set_percentage
      target:
        entity_id: fan.ventilairsec
      data:
        percentage: 100

# Reduce ventilation when humidity is normal
  - trigger:
      platform: numeric_state
      entity_id: sensor.ventilairsec_humidity
      below: 45
    action:
      service: fan.set_percentage
      target:
        entity_id: fan.ventilairsec
      data:
        percentage: 50
```

## Troubleshooting

### Addon Won't Start
- Check USB cable connection
- Verify serial port is correct (`/dev/ttyUSB0`, `/dev/ttyUSB1`, etc.)
- Check addon logs for error messages

### No Devices Found
- Ensure Enocean dongle is powered on
- Verify devices are within range (typical Enocean range: 300m outdoor, 40m indoor)
- Check dongle LED status
- Enable debug logging for detailed diagnostics

### Serial Port Not Available
```bash
# Find available serial ports
ls -la /dev/tty*

# Check USB devices
lsusb
```

### Enable Debug Mode
Set `debug_logging: true` in addon configuration to get detailed logs showing:
- Serial communication
- Packet parsing
- Device detection
- Configuration details

## Architecture Support

This addon is built for multiple architectures:
- **amd64**: Intel/AMD x86-64 systems
- **armv7**: 32-bit ARM (Raspberry Pi 2/3)
- **arm64**: 64-bit ARM (Raspberry Pi 4+)

Automatic selection based on your Home Assistant hardware.

## Performance

- **CPU**: Minimal usage (~1-2% on average)
- **Memory**: ~50-100 MB
- **Network**: Minimal (local socket communication)
- **Disk**: ~200 MB for addon + logs

## Support and Issues

For bug reports, feature requests, or general support:
- GitHub Issues: https://github.com/fortinric88/Ventilairsec2HA/issues
- Documentation: https://github.com/fortinric88/Ventilairsec2HA

## License

This addon is part of the Ventilairsec2HA project.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Happy ventilating!** 🌬️
