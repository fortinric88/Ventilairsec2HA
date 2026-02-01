#!/usr/bin/env python3
# Copyright (c) 2024 fortinric88. See LICENSE for further details.
"""Main entry point for Ventilairsec Enocean addon - Home Assistant overlay"""

import logging
import sys
import os
import traceback
import copy
import argparse
from configparser import ConfigParser
from pathlib import Path

# Setup paths
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

# Check for bashio availability in Home Assistant context
try:
    import bashio
    IN_HA_ADDON = True
except ImportError:
    IN_HA_ADDON = False


conf = {
    'debug': False,
    'config': ['/etc/ventilairsec/enoceanmqtt.conf'],
    'logfile': os.path.join(APP_DIR, '..', 'enoceanmqtt.log'),
    'mqtt_broker': 'localhost',
    'mqtt_port': 1883,
    'mqtt_user': '',
    'mqtt_password': '',
}


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('--debug', help='enable console debugging', action='store_true')
    parser.add_argument('--logfile', help='set log file location')
    parser.add_argument('config', help='specify config file[s]', nargs='*')
    args = vars(parser.parse_args())
    return args


def validate_config(config):
    """Validate critical configuration parameters"""
    errors = []
    
    # Validate MQTT port
    if 'mqtt_port' in config:
        try:
            port = int(config['mqtt_port'])
            if not (1 <= port <= 65535):
                errors.append(f"Invalid MQTT port: {port} (must be 1-65535)")
        except (ValueError, TypeError):
            errors.append(f"MQTT port must be an integer, got: {config['mqtt_port']}")
    
    # Validate serial rate
    if 'serial_rate' in config:
        try:
            rate = int(config['serial_rate'])
            valid_rates = [9600, 19200, 38400, 57600, 115200]
            if rate not in valid_rates:
                logging.warning("Serial rate %d is not standard. Standard rates: %s", rate, valid_rates)
        except (ValueError, TypeError):
            errors.append(f"Serial rate must be an integer, got: {config['serial_rate']}")
    
    # Validate MQTT broker hostname/IP
    if 'mqtt_broker' in config:
        broker = config['mqtt_broker']
        if not isinstance(broker, str) or len(broker) == 0:
            errors.append(f"MQTT broker must be a non-empty string, got: {broker}")
    
    # Validate serial port exists
    if 'serial_port' in config:
        serial_port = config['serial_port']
        if not isinstance(serial_port, str) or not serial_port.startswith('/dev/'):
            errors.append(f"Serial port must be a valid device path, got: {serial_port}")
    
    if errors:
        for error in errors:
            logging.error("Configuration validation error: %s", error)
        return False
    
    return True


def load_config_file(config_files):
    """Load sensor and general configuration from given config files"""
    sensors = []
    global_config = {}
    
    config = ConfigParser()
    config.read(config_files)
    
    # Load global configuration
    if config.has_section('global'):
        global_config = dict(config.items('global'))
    
    # Load sensor configurations
    for section in config.sections():
        if section.startswith('sensor:'):
            sensor_name = section[7:]  # Remove 'sensor:' prefix
            sensor_config = dict(config.items(section))
            sensor_config['name'] = sensor_name
            sensors.append(sensor_config)
    
    return sensors, global_config


def setup_logging(log_filename='', log_level=logging.INFO):
    """Initialize python logging infrastructure"""
    # Create formatter
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    
    # Set root logger to lowest log level
    logging.getLogger().setLevel(log_level)
    
    # Create console and log file handlers
    log_console = logging.StreamHandler(sys.stdout)
    log_console.setFormatter(log_formatter)
    log_console.setLevel(log_level)
    logging.getLogger().addHandler(log_console)
    
    if log_filename:
        try:
            log_file = logging.FileHandler(log_filename)
            log_file.setLevel(log_level)
            log_file.setFormatter(log_formatter)
            logging.getLogger().addHandler(log_file)
            logging.info("Logging to file: %s", log_filename)
        except (IOError, OSError) as err:
            logging.warning("Cannot create log file %s: %s", log_filename, err)


def get_ha_config():
    """Get Home Assistant addon configuration via bashio"""
    if not IN_HA_ADDON:
        return {}
    
    ha_config = {}
    try:
        # MQTT configuration
        if bashio.config('mqtt_broker'):
            ha_config['mqtt_broker'] = bashio.config('mqtt_broker')
        if bashio.config('mqtt_port'):
            ha_config['mqtt_port'] = int(bashio.config('mqtt_port'))
        if bashio.config('mqtt_user'):
            ha_config['mqtt_user'] = bashio.config('mqtt_user')
        if bashio.config('mqtt_password'):
            ha_config['mqtt_password'] = bashio.config('mqtt_password')
        
        # Serial configuration
        if bashio.config('serial_port'):
            ha_config['serial_port'] = bashio.config('serial_port')
        if bashio.config('serial_rate'):
            ha_config['serial_rate'] = int(bashio.config('serial_rate'))
    except Exception as err:
        logging.warning("Could not load Home Assistant config: %s", err)
    
    return ha_config


def main():
    """Entry point if called as an executable"""
    # Parse command line arguments
    conf.update(parse_args())
    
    # Get Home Assistant configuration if available
    if IN_HA_ADDON:
        conf.update(get_ha_config())
    
    # Setup logger
    setup_logging(conf.get('logfile', ''), logging.DEBUG if conf.get('debug') else logging.INFO)
    
    # Validate configuration before proceeding
    if not validate_config(conf):
        logging.error("Configuration validation failed. Aborting.")
        return False
    
    # Load config file
    config_files = conf.get('config', [])
    if not config_files:
        config_files = ['/etc/ventilairsec/enoceanmqtt.conf']
    
    sensors, global_config = load_config_file(config_files)
    conf.update(global_config)
    
    # Validate again after loading from file
    if not validate_config(conf):
        logging.error("Configuration validation failed after loading file. Aborting.")
        return False
    
    logging.info("Configuration loaded and validated: %d sensors found", len(sensors))
    
    # Select the overlay (Home Assistant)
    try:
        from communicator.homeassistant_communicator import HACommunicator
    except ImportError:
        logging.error("Unable to import Home Assistant communicator")
        logging.error("Make sure all dependencies are installed")
        return False
    
    logging.info("Selected overlay: Home Assistant")
    
    try:
        com = HACommunicator(conf, sensors)
        com.run()
    except KeyboardInterrupt:
        logging.info("Received SIGINT, shutting down...")
        return True
    except Exception:
        logging.error(traceback.format_exc())
        return False
    
    return True


# Check for execution
if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
