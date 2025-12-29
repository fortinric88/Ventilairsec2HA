# EnOcean Pi GPIO Configuration Guide

## Overview

The Ventilairsec Enocean addon now supports EnOcean Pi modules connected via GPIO on Raspberry Pi. This allows direct connection without requiring a USB dongle.

## Supported Communication Methods

### 1. Serial (USB/ACM) - Default
- USB Enocean dongle (TCM310, TCM320, etc.)
- Default and most compatible option
- No GPIO wiring required

### 2. GPIO - EnOcean Pi Module

#### SPI Mode (Recommended for RPi)
```
EnOcean Pi Pin    Raspberry Pi GPIO
---------         --------
CLK     →         GPIO11 (SCLK)
MOSI    →         GPIO10 (MOSI)
MISO    →         GPIO9  (MISO)
CS      →         GPIO24 (customizable)
GND     →         GND
VCC     →         3.3V
```

#### UART Mode
```
EnOcean Pi Pin    Raspberry Pi GPIO
---------         --------
TX      →         GPIO14 or custom (RX pin)
RX      →         GPIO15 or custom (TX pin)
GND     →         GND
VCC     →         3.3V
```

#### I2C Mode
```
EnOcean Pi Pin    Raspberry Pi GPIO
---------         --------
SCL     →         GPIO3  (SCL)
SDA     →         GPIO2  (SDA)
GND     →         GND
VCC     →         3.3V
```

## Configuration in Home Assistant

### Step 1: Choose Communication Type

In **Settings → Add-ons & Services → Ventilairsec Enocean → Configuration**:

Set `communication_type` to one of:
- `serial` (default)
- `gpio`

### Step 2: Configure Serial (if using USB)

If `communication_type: serial`:
- **serial_port**: `/dev/ttyUSB0` (or `/dev/ttyUSB1`, `/dev/ttyACM0`, etc.)
- **serial_rate**: `115200` (standard for Enocean)

### Step 3: Configure GPIO (if using EnOcean Pi)

If `communication_type: gpio`:

#### Common GPIO Options

| Option | Type | Default | Range | Description |
|--------|------|---------|-------|-------------|
| `gpio_mode` | select | `spi` | spi/uart/i2c | Communication protocol |
| `gpio_tx_pin` | integer | `24` | 0-28 | TX pin (UART) or CS (SPI) |
| `gpio_rx_pin` | integer | `25` | 0-28 | RX pin (UART) |
| `gpio_reset_pin` | integer | `17` | 0-28 | RESET pin (0 to disable) |

#### SPI Configuration Example
```yaml
communication_type: gpio
gpio_mode: spi
gpio_tx_pin: 24      # CS (Chip Select)
gpio_reset_pin: 17   # RESET
```

#### UART Configuration Example
```yaml
communication_type: gpio
gpio_mode: uart
gpio_tx_pin: 24      # RX (receive)
gpio_rx_pin: 25      # TX (transmit)
gpio_reset_pin: 17   # RESET
```

#### I2C Configuration Example
```yaml
communication_type: gpio
gpio_mode: i2c
gpio_reset_pin: 17   # RESET (optional)
```

## GPIO Pin Reference for Raspberry Pi

### GPIO Pin Layout
```
Physical Pin    BCM GPIO    Pin Name    Notes
------          --------    --------    -----
3               2           SDA         I2C Data
5               3           SCL         I2C Clock
8               14          TXD         UART Transmit
10              15          RXD         UART Receive
11              17          GPIO17      General Purpose
13              27          GPIO27      General Purpose
16              23          GPIO23      General Purpose
18              24          GPIO24      General Purpose (SPI CS)
19              10          MOSI        SPI Master Out
21              9           MISO        SPI Slave In
23              11          SCLK        SPI Clock
```

### Hardware Requirements

- **Power**: 3.3V (NOT 5V - GPIO on RPi operates at 3.3V)
- **Ground**: Common GND to all devices
- **Signal**: Pull-up resistors may be needed (check EnOcean module specs)

## Installation Steps

### 1. Prepare Hardware

#### For SPI:
- Connect EnOcean Pi to SPI pins
- Verify voltage levels (3.3V)
- Add pull-up resistors if needed

#### For UART:
- Connect TX/RX to GPIO pins
- Ensure 3.3V voltage
- Add pull-ups (47kΩ typical)

#### For I2C:
- Connect SDA/SCL to GPIO2/GPIO3
- Add 4.7kΩ pull-up resistors
- Verify I2C address (0x80 for TCM modules)

### 2. Configure Addon

1. Go to **Settings → Add-ons & Services → Ventilairsec Enocean**
2. Click **Configuration**
3. Set:
   - `communication_type`: `gpio`
   - `gpio_mode`: Choose `spi`, `uart`, or `i2c`
   - Pin numbers (matching your wiring)
4. Click **Save**

### 3. Start Addon

1. Go to **Add-ons** tab
2. Find "Ventilairsec Enocean"
3. Click **Start**
4. Check logs for initialization messages

### 4. Verify Connection

Look for messages like:
```
GPIO communication initialized (mode=spi)
GPIO Bridge initialized (mode=spi, TX=24, RX=25)
```

## Troubleshooting

### GPIO Not Accessible
**Error**: `Permission denied` or `Device or resource busy`

**Solutions**:
- Addon needs elevated permissions (check `privileged` settings)
- Another process might be using GPIO (check running addons)
- GPIO not exported properly (check `/sys/class/gpio/`)

### SPI Communication Issues
**Error**: `No such file or directory` (/dev/spidev0.0)

**Solutions**:
- Check if SPI is enabled in Raspberry Pi settings
- Verify wiring (CLK, MOSI, MISO)
- Check CS pin (GPIO24 by default)

### UART Communication Issues
**Error**: `Port or device busy`

**Solutions**:
- Disable other UART services
- Check if `/dev/ttyAMA0` is in use
- For custom pins, verify GPIO software UART (bit-banging)

### I2C Communication Issues
**Error**: `i2c_msg.buf is empty`

**Solutions**:
- Check I2C address (0x80 for TCM)
- Verify pull-up resistors present
- Check signal integrity with oscilloscope

### Module Not Detected
**Symptom**: Addon starts but no devices found

**Solutions**:
1. Check power supply (3.3V minimum, 500mA recommended)
2. Verify GND connection
3. Check signal lines with multimeter
4. Try `gpio_reset_pin` toggle if supported
5. Enable debug logging for detailed output

## Advanced Configuration

### Enable Debug Logging

Set `debug_logging: true` to see detailed GPIO communication:

```
[DEBUG] GPIO Bridge initialized
[DEBUG] SPI read: 0x55 0x00 0x0A ...
[DEBUG] Packet received: RORG=0xA5, ID=0x12345678
```

### Multiple Enocean Modules

Not currently supported in single addon instance. Workaround:
- Install addon twice with different slugs
- Use different GPIO pins for each

### Performance Tuning

```yaml
cycle_time: 0.1        # Faster cycle (more CPU usage)
debug_logging: false   # Disable for better performance
```

## Supported Enocean Modules

### Known Compatible
- **EnOcean TCM110** (SPI, I2C)
- **EnOcean TCM310** (I2C, UART)
- **EnOcean TCM320** (UART, I2C)
- **EnOcean USB 300** (Serial only)
- **EnOcean Pi** (SPI)

### Potentially Compatible
- Any module with SPI/UART/I2C interface
- Operating at 3.3V
- Enocean protocol compatible

## Power Consumption

| Mode | Current | Notes |
|------|---------|-------|
| GPIO SPI | 50-100 mA | Most efficient |
| GPIO UART | 60-120 mA | Medium efficiency |
| GPIO I2C | 30-80 mA | Most efficient, needs pull-ups |
| USB Serial | 100-200 mA | External power often available |

## Switching Between Modes

To switch from USB to GPIO:
1. Stop the addon
2. Change `communication_type` from `serial` to `gpio`
3. Update GPIO pins if needed
4. Save and restart

To switch from GPIO to USB:
1. Stop the addon
2. Change `communication_type` from `gpio` to `serial`
3. Plug in USB dongle
4. Save and restart

## Additional Resources

- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)
- [EnOcean Protocol Specifications](https://www.enocean.com/en/)
- [TCM Module Datasheets](https://www.enocean.com/en/products/enocean-modules/tcm-3xx/)

---

**For issues or questions**: Check the addon logs or submit a GitHub issue.
