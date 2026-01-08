"""Base communicator for enocean protocol handling"""

import logging
import json
import paho.mqtt.client as mqtt
from abc import ABC, abstractmethod


class Communicator(ABC):
    """Base communicator class providing MQTT interface to enocean packets"""
    
    def __init__(self, config, sensors):
        """Initialize the communicator
        
        Args:
            config: Configuration dictionary
            sensors: List of sensor configurations
        """
        self.config = config
        self.sensors = sensors
        self.mqtt = None
        
        logging.info("Initializing communicator with %d sensors", len(sensors))
    
    def setup_mqtt(self):
        """Setup MQTT connection"""
        broker = self.config.get('mqtt_broker', 'localhost')
        port = int(self.config.get('mqtt_port', 1883))
        user = self.config.get('mqtt_user', '')
        password = self.config.get('mqtt_password', '')
        
        self.mqtt = mqtt.Client()
        
        if user:
            self.mqtt.username_pw_set(user, password)
        
        self.mqtt.on_connect = self._on_mqtt_connect
        self.mqtt.on_disconnect = self._on_mqtt_disconnect
        self.mqtt.on_message = self._on_mqtt_message
        
        try:
            self.mqtt.connect(broker, port, 60)
            self.mqtt.loop_start()
            logging.info("Connected to MQTT broker at %s:%d", broker, port)
        except Exception as err:
            logging.error("Failed to connect to MQTT broker: %s", err)
            raise
    
    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """Callback for MQTT connection"""
        if rc == 0:
            logging.info("MQTT connection successful")
        else:
            logging.error("MQTT connection failed with code: %d", rc)
    
    def _on_mqtt_disconnect(self, client, userdata, rc):
        """Callback for MQTT disconnection"""
        if rc != 0:
            logging.warning("Unexpected MQTT disconnection with code: %d", rc)
    
    def _on_mqtt_message(self, client, userdata, msg):
        """Callback for incoming MQTT messages"""
        logging.debug("Received MQTT message on %s: %s", msg.topic, msg.payload)
    
    def publish(self, topic, payload, retain=False):
        """Publish to MQTT topic
        
        Args:
            topic: MQTT topic
            payload: Message payload
            retain: Retain message flag
        """
        if self.mqtt:
            self.mqtt.publish(topic, payload, retain=retain)
    
    @abstractmethod
    def run(self):
        """Main run loop - must be implemented by subclasses"""
        raise NotImplementedError
