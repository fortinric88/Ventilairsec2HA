#!/usr/bin/env bash
set -e

# Colors for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

source /usr/lib/bashio/bashio.sh

bashio::log.info "Starting Ventilairsec Enocean addon..."

# Get configuration from Home Assistant
SERIAL_PORT=$(bashio::config 'serial_port')
SERIAL_RATE=$(bashio::config 'serial_rate')
DEBUG_LOGGING=$(bashio::config 'debug_logging')
MQTT_BROKER=$(bashio::config 'mqtt_broker')
MQTT_PORT=$(bashio::config 'mqtt_port')
MQTT_USER=$(bashio::config 'mqtt_user')
MQTT_PASSWORD=$(bashio::config 'mqtt_password')

bashio::log.info "Configuration loaded:"
bashio::log.info "  Serial port: $SERIAL_PORT"
bashio::log.info "  Serial rate: $SERIAL_RATE baud"
bashio::log.info "  MQTT broker: $MQTT_BROKER:$MQTT_PORT"
bashio::log.info "  Debug mode: $DEBUG_LOGGING"

# Create required directories
mkdir -p /var/log/ventilairsec
mkdir -p /var/lib/ventilairsec
mkdir -p /etc/ventilairsec

# Create configuration file for enoceanmqtt
# Use restrictive permissions (0600) for security - only root can read/write
cat > /etc/ventilairsec/enoceanmqtt.conf << EOF
[global]
mqtt_broker = $MQTT_BROKER
mqtt_port = $MQTT_PORT
mqtt_user = $MQTT_USER
mqtt_password = $MQTT_PASSWORD
serial_port = $SERIAL_PORT
serial_rate = $SERIAL_RATE
debug = $DEBUG_LOGGING
overlay = ha
db_file = /var/lib/ventilairsec/device_db.json
ha_discovery_prefix = homeassistant

EOF

# Set restrictive permissions on config file containing credentials
chmod 0600 /etc/ventilairsec/enoceanmqtt.conf

bashio::log.info "Configuration file created at /etc/ventilairsec/enoceanmqtt.conf (permissions: 0600)"

# Check serial port availability with timeout
bashio::log.info "Checking for serial port: $SERIAL_PORT"
TIMEOUT=30
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
    if [ -c "$SERIAL_PORT" ]; then
        bashio::log.info "Serial port detected: $SERIAL_PORT"
        break
    fi
    
    bashio::log.warning "Serial port $SERIAL_PORT not available (waiting: ${ELAPSED}s/$TIMEOUT)"
    sleep 2
    ELAPSED=$((ELAPSED + 2))
done

if [ ! -c "$SERIAL_PORT" ]; then
    bashio::log.error "Serial port $SERIAL_PORT not found after ${TIMEOUT}s timeout"
    bashio::log.error "Please verify your USB device is connected"
    exit 1
fi

bashio::log.info "Starting Enocean daemon..."

# Start the main application
cd /app
python3 enoceanmqtt.py --config /etc/ventilairsec/enoceanmqtt.conf $([ "$DEBUG_LOGGING" = "true" ] && echo "--debug")

