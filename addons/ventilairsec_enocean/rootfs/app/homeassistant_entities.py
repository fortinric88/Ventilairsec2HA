"""
Module d'intégration Home Assistant - Classes pour les entités
"""

import logging
from typing import Dict, Any, Optional, Callable
from abc import ABC, abstractmethod

logger = logging.getLogger('ventilairsec_enocean.homeassistant')

class Entity(ABC):
    """Classe de base pour les entités Home Assistant"""
    
    def __init__(self, unique_id: str, name: str, device_id: str):
        self.unique_id = unique_id
        self.name = name
        self.device_id = device_id
        self.state: Optional[Any] = None
        self.attributes: Dict[str, Any] = {}
        self.available = True
        self.callbacks: list[Callable] = []
    
    @abstractmethod
    def update(self, payload: Dict[str, Any]):
        """Mettre à jour l'état de l'entité"""
        pass
    
    def add_callback(self, callback: Callable):
        """Ajouter un callback de mise à jour"""
        self.callbacks.append(callback)
    
    def notify_state_changed(self):
        """Notifier les changements d'état"""
        for callback in self.callbacks:
            try:
                callback(self)
            except Exception as e:
                logger.error(f"Erreur lors de l'appel du callback: {e}")


class TemperatureSensor(Entity):
    """Capteur de température"""
    
    def __init__(self, unique_id: str, name: str, device_id: str):
        super().__init__(unique_id, name, device_id)
        self.unit_of_measurement = "°C"
        self.device_class = "temperature"
    
    def update(self, payload: Dict[str, Any]):
        """Mettre à jour la température"""
        # Parser les données selon le format du payload
        if 'temperature' in payload:
            new_state = float(payload['temperature'])
            if self.state != new_state:
                self.state = new_state
                self.notify_state_changed()


class HumiditySensor(Entity):
    """Capteur d'humidité"""
    
    def __init__(self, unique_id: str, name: str, device_id: str):
        super().__init__(unique_id, name, device_id)
        self.unit_of_measurement = "%"
        self.device_class = "humidity"
    
    def update(self, payload: Dict[str, Any]):
        """Mettre à jour l'humidité"""
        if 'humidity' in payload:
            new_state = float(payload['humidity'])
            if self.state != new_state:
                self.state = new_state
                self.notify_state_changed()


class BinarySensor(Entity):
    """Capteur binaire"""
    
    def __init__(self, unique_id: str, name: str, device_id: str, device_class: str = "motion"):
        super().__init__(unique_id, name, device_id)
        self.device_class = device_class
    
    def update(self, payload: Dict[str, Any]):
        """Mettre à jour l'état binaire"""
        if 'state' in payload:
            new_state = bool(payload['state'])
            if self.state != new_state:
                self.state = new_state
                self.notify_state_changed()


class Fan(Entity):
    """Contrôle de ventilateur (VMI)"""
    
    def __init__(self, unique_id: str, name: str, device_id: str):
        super().__init__(unique_id, name, device_id)
        self.device_class = "fan"
        self.supported_features = ["turn_on", "turn_off", "set_speed"]
        self.speed_range = [0, 100]
        self.percentage_step = 1
    
    def update(self, payload: Dict[str, Any]):
        """Mettre à jour l'état du ventilateur"""
        if 'speed' in payload:
            new_state = int(payload['speed'])
            if self.state != new_state:
                self.state = new_state
                self.notify_state_changed()
    
    async def set_speed(self, speed: int):
        """Définir la vitesse du ventilateur"""
        if 0 <= speed <= 100:
            self.state = speed
            self.notify_state_changed()


class Switch(Entity):
    """Commutateur/Relais"""
    
    def __init__(self, unique_id: str, name: str, device_id: str):
        super().__init__(unique_id, name, device_id)
        self.device_class = "outlet"
    
    def update(self, payload: Dict[str, Any]):
        """Mettre à jour l'état du commutateur"""
        if 'state' in payload:
            new_state = bool(payload['state'])
            if self.state != new_state:
                self.state = new_state
                self.notify_state_changed()
    
    async def turn_on(self):
        """Allumer"""
        self.state = True
        self.notify_state_changed()
    
    async def turn_off(self):
        """Éteindre"""
        self.state = False
        self.notify_state_changed()


class VentilairsecDevice:
    """Représentation d'un appareil Ventilairsec/VMI"""
    
    def __init__(self, device_id: str, sender_id: int, device_type: str):
        self.device_id = device_id
        self.sender_id = sender_id
        self.device_type = device_type
        self.entities: Dict[str, Entity] = {}
        self.name = f"Ventilairsec {sender_id:08x}"
    
    def add_entity(self, entity: Entity):
        """Ajouter une entité au device"""
        self.entities[entity.unique_id] = entity
    
    def get_entity(self, unique_id: str) -> Optional[Entity]:
        """Récupérer une entité"""
        return self.entities.get(unique_id)
    
    def update_from_payload(self, payload: Dict[str, Any]):
        """Mettre à jour toutes les entités avec le payload"""
        for entity in self.entities.values():
            try:
                entity.update(payload)
            except Exception as e:
                logger.error(f"Erreur lors de la mise à jour de {entity.unique_id}: {e}")
