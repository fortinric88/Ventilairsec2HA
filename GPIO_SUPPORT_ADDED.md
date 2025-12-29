# GPIO Support Added - Summary of Changes

**Date**: December 29, 2025  
**Feature**: EnOcean Pi GPIO Support  
**Status**: ✅ IMPLEMENTED

---

## What's New

The addon now supports **EnOcean Pi modules connected via GPIO** on Raspberry Pi, in addition to the existing USB dongle support.

### Communication Methods Supported

| Method | Hardware | Mode | Status |
|--------|----------|------|--------|
| USB Serial | Enocean USB dongle | Serial | ✅ (existing) |
| **GPIO SPI** | **EnOcean Pi** | **SPI** | ✅ **NEW** |
| **GPIO UART** | **EnOcean Pi** | **UART** | ✅ **NEW** |
| **GPIO I2C** | **EnOcean Pi** | **I2C** | ✅ **NEW** |

---

## Files Modified

### 1. `addon.yaml` - Added GPIO Configuration

**Changes**:
- Added `communication_type` option (select: serial/gpio)
- Added GPIO-specific options:
  - `gpio_mode`: SPI/UART/I2C mode
  - `gpio_tx_pin`: Pin for TX or CS
  - `gpio_rx_pin`: Pin for RX
  - `gpio_reset_pin`: Pin for module reset
- Added GPIO device access (`/dev/mem`, `/dev/gpiomem`)

**Before**: 
```yaml
options:
  serial_port: /dev/ttyUSB0
  serial_rate: 115200
```

**After**:
```yaml
options:
  communication_type: serial         # ← NEW
  serial_port: /dev/ttyUSB0
  serial_rate: 115200
  gpio_mode: spi                    # ← NEW
  gpio_tx_pin: 24                   # ← NEW
  gpio_rx_pin: 25                   # ← NEW
  gpio_reset_pin: 17                # ← NEW
  socket_port: 55006
  cycle_time: 0.3
  debug_logging: false
```

### 2. `enocean_daemon.py` - Added GPIO Support

**Changes**:
- Modified `__init__()` to detect communication type
- Added `_initialize_gpio()` method
- Updated `_process_receive()` to handle both serial and GPIO
- Split into `_process_receive_serial()` and `_process_receive_gpio()`
- Updated `stop()` to properly shutdown GPIO

**Key Methods**:
```python
self.communication_type = config.get('communication_type', 'serial')

# Initialize based on type
if self.communication_type == 'gpio':
    await self._initialize_gpio()
else:
    await self._initialize_serial()
```

### 3. `enocean_gpio.py` - NEW FILE

**Purpose**: Handle GPIO communication with EnOcean modules

**Features**:
- `EnoceanGPIOBridge` class for GPIO operations
- Support for 3 modes:
  - **SPI**: Using Adafruit Blinka (via `busio.SPI`)
  - **UART**: Using RPi.GPIO (bit-banged)
  - **I2C**: Using Adafruit Blinka (via `busio.I2C`)

**Methods**:
```python
async def initialize()        # Setup GPIO pins
async def read_packet()       # Read Enocean packet
async def write_packet()      # Send Enocean packet
async def _init_spi()        # SPI initialization
async def _init_uart()       # UART initialization
async def _init_i2c()        # I2C initialization
def shutdown()               # Cleanup GPIO
```

### 4. `requirements.txt` - Added GPIO Libraries

**New Dependencies**:
```
gpiozero==2.0.1          # GPIO abstraction
RPi.GPIO==0.7.0          # Raspberry Pi GPIO access
adafruit-blinka==8.2.0   # Adafruit unified GPIO interface
```

### 5. `repository.json` - Updated Configuration Schema

**Changes**:
- Added `communication_type` to options
- Added all GPIO pin options
- Updated schema with new types
- Added `/dev/mem` and `/dev/gpiomem` to devices

### 6. `GPIO_SETUP.md` - NEW Documentation

**Comprehensive guide including**:
- Wiring diagrams for each mode
- GPIO pin reference for Raspberry Pi
- Installation steps
- Configuration examples
- Troubleshooting section
- Hardware requirements
- Power consumption specs

---

## Configuration Examples

### Option 1: Serial USB (Default - No Change)

```yaml
communication_type: serial
serial_port: /dev/ttyUSB0
serial_rate: 115200
```

### Option 2: GPIO SPI (EnOcean Pi)

```yaml
communication_type: gpio
gpio_mode: spi
gpio_tx_pin: 24      # Chip Select
gpio_reset_pin: 17   # Module Reset
```

### Option 3: GPIO UART (EnOcean Pi)

```yaml
communication_type: gpio
gpio_mode: uart
gpio_tx_pin: 24      # RX (receive)
gpio_rx_pin: 25      # TX (transmit)
gpio_reset_pin: 17   # Reset
```

### Option 4: GPIO I2C (EnOcean Pi)

```yaml
communication_type: gpio
gpio_mode: i2c
gpio_reset_pin: 17   # Reset (optional)
```

---

## Hardware Wiring

### SPI Mode (Recommended)
```
EnOcean Pi          RPi GPIO
CLK     ────→       GPIO11 (SCLK)
MOSI    ────→       GPIO10 (MOSI)
MISO    ────→       GPIO9  (MISO)
CS      ────→       GPIO24 (configurable)
GND     ────→       GND
3.3V    ────→       3.3V (NOT 5V!)
```

### UART Mode
```
EnOcean Pi          RPi GPIO
TX      ────→       GPIO24 or custom
RX      ────→       GPIO25 or custom
GND     ────→       GND
3.3V    ────→       3.3V (NOT 5V!)
```

### I2C Mode
```
EnOcean Pi          RPi GPIO
SDA     ────→       GPIO2 (SDA)
SCL     ────→       GPIO3 (SCL)
GND     ────→       GND
3.3V    ────→       3.3V (NOT 5V!)
+ 4.7kΩ pull-ups needed
```

---

## Benefits

✅ **More Flexible**: Choose between USB or GPIO  
✅ **Lower Cost**: No need for USB dongle (if using GPIO)  
✅ **Direct Integration**: EnOcean Pi Pi HAT support  
✅ **Multiple Modes**: SPI, UART, or I2C options  
✅ **Backward Compatible**: Existing USB setups still work  
✅ **Well Documented**: Complete setup guide included  

---

## Testing Recommendations

### Before Production Use

1. **Test GPIO access**:
   ```bash
   # Check GPIO availability
   ls -la /sys/class/gpio/
   ```

2. **Verify wiring**:
   - Check all connections with multimeter
   - Ensure 3.3V (NOT 5V!)
   - Common GND

3. **Check logs**:
   ```
   Enable debug_logging: true
   Look for "GPIO communication initialized"
   ```

4. **Monitor performance**:
   - Check CPU usage
   - Monitor temperature
   - Verify packet reception

---

## Known Limitations

- ⚠️ Bit-banged UART slower than hardware UART
- ⚠️ I2C requires proper pull-up resistors
- ⚠️ Not compatible with other GPIO-using addons
- ⚠️ Requires elevated permissions (privileged addon)

---

## Backward Compatibility

✅ **Fully backward compatible** - Existing USB configurations continue to work without any changes.

Default setting remains `communication_type: serial`.

---

## Documentation

New file created: **[GPIO_SETUP.md](./GPIO_SETUP.md)**

Contains:
- Complete hardware setup guide
- GPIO pin reference
- Configuration examples for each mode
- Troubleshooting section
- Power consumption specifications
- Supported Enocean modules

---

## Next Steps

1. **Test GPIO Configuration**:
   - Configure `communication_type: gpio`
   - Wire EnOcean Pi per GPIO_SETUP.md
   - Start addon and check logs

2. **Enable Debug Logging**:
   - Set `debug_logging: true`
   - Monitor GPIO communication
   - Verify packet reception

3. **Fine-tune Settings**:
   - Adjust GPIO pins if needed
   - Optimize cycle time for performance
   - Set appropriate log level

---

## Version Info

- **Addon Version**: Still 1.0.0 (feature addition)
- **Python Version**: 3.9+
- **New Dependencies**: gpiozero, RPi.GPIO, adafruit-blinka
- **Home Assistant**: 2023.10.0+

---

## Support

For GPIO-related issues:
1. Check **GPIO_SETUP.md** troubleshooting section
2. Enable debug logging
3. Review addon logs
4. Submit GitHub issue with logs

---

**GPIO Support Successfully Added!** ✅

Users can now choose between:
- 🔌 USB dongle (existing)
- 🔧 GPIO SPI/UART/I2C (NEW)
