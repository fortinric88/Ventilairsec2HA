# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-29

### Added

- Initial Home Assistant addon release
- Full Enocean protocol support (4BS and 1BS packets)
- VMI Purevent Ventilairsec integration (D1079-01-00)
- Support for generic Enocean sensors (A5-20-01, D5-00-01)
- Home Assistant entity creation (sensors, fans, switches, binary sensors)
- Multi-architecture support (amd64, armv7, arm64)
- Serial port configuration with dynamic device detection
- Web socket API for device communication
- Comprehensive logging and debugging options
- Device discovery and automatic entity registration
- Temperature, humidity, and air quality monitoring
- Fan speed control and status reporting
- CRC verification for data integrity
- YAML configuration with schema validation

### Features

- **Enocean Daemon**: Background service handling serial communication at 115200 baud
- **Device Profiles**: Support for multiple Enocean device types
- **Entity Management**: Automatic Home Assistant entity creation
- **Configuration Options**:
  - Serial port selection (/dev/ttyUSB0-1, /dev/ttyACM0-1)
  - Baud rate configuration
  - Cycle time adjustment
  - Debug logging toggle

### Architecture Support

- amd64 (Intel/AMD x86-64)
- armv7 (ARM 32-bit, Raspberry Pi 2-3)
- arm64 (ARM 64-bit, Raspberry Pi 4+)

---

## Future Versions

### [1.1.0] - Planned

- Additional Enocean device profiles
- Home Assistant history statistics
- Performance optimizations
- Extended troubleshooting guides
