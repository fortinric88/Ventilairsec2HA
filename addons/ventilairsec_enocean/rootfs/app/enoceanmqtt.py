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
        if bashio::config('mqtt_broker'):
            ha_config['mqtt_broker'] = bashio::config('mqtt_broker')
        if bashio::config('mqtt_port'):
            ha_config['mqtt_port'] = int(bashio::config('mqtt_port'))
        if bashio::config('mqtt_user'):
            ha_config['mqtt_user'] = bashio::config('mqtt_user')
        if bashio::config('mqtt_password'):
            ha_config['mqtt_password'] = bashio::config('mqtt_password')
        
        # Serial configuration
        if bashio::config('serial_port'):
            ha_config['serial_port'] = bashio::config('serial_port')
        if bashio::config('serial_rate'):
            ha_config['serial_rate'] = int(bashio::config('serial_rate'))
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
    
    # Load config file
    config_files = conf.get('config', [])
    if not config_files:
        config_files = ['/etc/ventilairsec/enoceanmqtt.conf']
    
    sensors, global_config = load_config_file(config_files)
    conf.update(global_config)
    
    logging.info("Configuration loaded: %d sensors found", len(sensors))
    
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
