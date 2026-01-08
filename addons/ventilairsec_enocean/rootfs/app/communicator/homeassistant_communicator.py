"""Home Assistant communicator module"""

import logging
import os
import json
from pathlib import Path
from communicator import Communicator


class DeviceManager:
    """Manages device database for Home Assistant"""
    
    def __init__(self, config):
        """Initialize device manager
        
        Args:
            config: Configuration dictionary
        """
        self.db_file = config.get('db_file', '/var/lib/ventilairsec/device_db.json')
        self.devices = self._load_db()
        logging.info("Device database loaded from %s", self.db_file)
    
    def _load_db(self):
        """Load device database from file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except Exception as err:
                logging.error("Failed to load device database: %s", err)
        return {}
    
    def _save_db(self):
        """Save device database to file"""
        try:
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            with open(self.db_file, 'w') as f:
                json.dump(self.devices, f, indent=4)
        except Exception as err:
            logging.error("Failed to save device database: %s", err)
    
    def add_device(self, address, device_info):
        """Add or update device in database
        
        Args:
            address: Device address
            device_info: Device information dictionary
        """
        self.devices[str(address)] = device_info
        self._save_db()
    
    def get_device(self, address):
        """Get device from database
        
        Args:
            address: Device address
            
        Returns:
            Device information or None
        """
        return self.devices.get(str(address))
    
    def get_all_devices(self):
        """Get all devices
        
        Returns:
            Dictionary of all devices
        """
        return self.devices


class HACommunicator(Communicator):
    """Home Assistant overlay for enocean communicator"""
    
    def __init__(self, config, sensors):
        """Initialize Home Assistant communicator
        
        Args:
            config: Configuration dictionary
            sensors: List of sensor configurations
        """
        super().__init__(config, sensors)
        self.device_manager = DeviceManager(config)
        self.setup_mqtt()
        
        # Home Assistant MQTT Discovery settings
        self.ha_discovery_prefix = config.get('ha_discovery_prefix', 'homeassistant')
        
        logging.info("Home Assistant communicator initialized")
    
    def discover_device(self, address, device_info):
        """Publish Home Assistant device discovery
        
        Args:
            address: Device address
            device_info: Device information
        """
        device_uid = device_info.get('uid', f"enocean_{address:08X}")
        device_name = device_info.get('name', f"Device {address:08X}")
        
        # Store in device manager
        self.device_manager.add_device(address, device_info)
        
        # Publish MQTT discovery message
        discovery_topic = f"{self.ha_discovery_prefix}/sensor/{device_uid}/config"
        
        config = {
            "name": device_name,
            "unique_id": device_uid,
            "device": {
                "identifiers": [device_uid],
                "name": device_name,
                "manufacturer": "EnOcean"
            },
            "state_topic": f"enocean/{device_uid}/state"
        }
        
        self.publish(discovery_topic, json.dumps(config), retain=True)
        logging.info("Device %s discovered: %s", device_uid, device_name)
    
    def publish_sensor(self, address, sensor_type, value):
        """Publish sensor reading
        
        Args:
            address: Device address
            sensor_type: Type of sensor
            value: Sensor value
        """
        device = self.device_manager.get_device(address)
        if not device:
            logging.warning("Unknown device: %08X", address)
            return
        
        device_uid = device.get('uid', f"enocean_{address:08X}")
        topic = f"enocean/{device_uid}/{sensor_type}"
        
        self.publish(topic, str(value), retain=True)
    
    def run(self):
        """Main run loop for Home Assistant overlay"""
        logging.info("Home Assistant communicator is running...")
        
        try:
            # Keep the loop alive
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Shutting down...")
            if self.mqtt:
                self.mqtt.loop_stop()
                self.mqtt.disconnect()
