"""
Pont Home Assistant - Intègre l'addon dans Home Assistant
"""

import logging
import asyncio
import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger('ventilairsec_enocean.bridge')

class HomeAssistantBridge:
    """Pont de communication avec Home Assistant"""
    
    def __init__(self, config: Dict[str, Any], daemon):
        """
        Initialiser le pont Home Assistant
        
        Args:
            config: Configuration Home Assistant
            daemon: Instance du daemon Enocean
        """
        self.config = config
        self.daemon = daemon
        self.running = False
        self.devices = {}
        self.last_update = {}
        
    async def initialize(self):
        """Initialiser la connexion avec Home Assistant"""
        try:
            host = self.config.get('host', 'supervisor')
            port = self.config.get('port', 8123)
            
            logger.info(f"Initialisation du pont vers Home Assistant ({host}:{port})")
            
            # Découvrir les appareils existants
            await self._discover_devices()
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du pont: {e}")
    
    async def _discover_devices(self):
        """Découvrir les appareils Enocean connus"""
        logger.info("Découverte des appareils Enocean...")
        
        # Charger depuis la configuration persistante
        config_file = '/var/lib/ventilairsec/devices.json'
        try:
            import json
            from pathlib import Path
            
            path = Path(config_file)
            if path.exists():
                with open(path, 'r') as f:
                    self.devices = json.load(f)
                logger.info(f"Appareils chargés: {list(self.devices.keys())}")
        except Exception as e:
            logger.warning(f"Impossible de charger les appareils: {e}")
    
    async def _save_devices(self):
        """Sauvegarder les appareils découverts"""
        try:
            import json
            from pathlib import Path
            
            path = Path('/var/lib/ventilairsec/devices.json')
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w') as f:
                json.dump(self.devices, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des appareils: {e}")
    
    def run(self):
        """Lancer le pont (thread de traitement)"""
        self.running = True
        logger.info("Pont Home Assistant lancé")
        
        while self.running:
            try:
                # Récupérer les paquets du daemon
                packet = self.daemon.get_received_packet()
                if packet:
                    self._process_packet(packet)
                
                asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Erreur dans le pont: {e}")
    
    def _process_packet(self, packet: Dict[str, Any]):
        """Traiter un paquet reçu"""
        if packet.get('type') != 'radio_message':
            return
        
        sender_id = packet.get('sender_id')
        payload = packet.get('payload', {})
        
        logger.debug(f"Paquet reçu de {sender_id:08x}: {payload}")
        
        # Créer ou mettre à jour l'appareil
        device_id = f"enocean_{sender_id:08x}"
        
        if device_id not in self.devices:
            self.devices[device_id] = {
                'id': device_id,
                'sender_id': sender_id,
                'discovered_at': datetime.now().isoformat(),
                'type': self._detect_device_type(payload),
                'last_update': datetime.now().isoformat()
            }
            logger.info(f"Nouvel appareil découvert: {device_id}")
            
            # Sauvegarder
            asyncio.create_task(self._save_devices())
        else:
            self.devices[device_id]['last_update'] = datetime.now().isoformat()
        
        # Parser et créer les entités Home Assistant
        self._create_entities(device_id, payload)
    
    def _detect_device_type(self, payload: Dict[str, Any]) -> str:
        """Détecter le type d'appareil basé sur le payload"""
        rorg = payload.get('rorg')
        
        if rorg == 0xA5:
            # 4BS - Capteurs multiples
            return 'thermostat_sensor'
        elif rorg == 0xD5:
            # 1BS - Capteurs simples
            return 'binary_sensor'
        elif rorg == 0xD2:
            # Variable - Généralement des variables
            return 'variable_sensor'
        else:
            return 'unknown'
    
    def _create_entities(self, device_id: str, payload: Dict[str, Any]):
        """Créer les entités Home Assistant pour ce paquet"""
        device_type = self.devices[device_id].get('type')
        
        if device_type == 'thermostat_sensor':
            self._parse_4bs_payload(device_id, payload)
        elif device_type == 'binary_sensor':
            self._parse_1bs_payload(device_id, payload)
    
    def _parse_4bs_payload(self, device_id: str, payload: Dict[str, Any]):
        """Parser payload 4BS (capteur thermique/humidité)"""
        db3 = payload.get('db3', 0)
        db2 = payload.get('db2', 0)
        db1 = payload.get('db1', 0)
        db0 = payload.get('db0', 0)
        
        # Exemple: VMI Purevent avec temp et humidité
        # Les interprétations exact dépendent du device spécifique
        
        logger.debug(f"4BS Data: DB3={db3:02x} DB2={db2:02x} DB1={db1:02x} DB0={db0:02x}")
    
    def _parse_1bs_payload(self, device_id: str, payload: Dict[str, Any]):
        """Parser payload 1BS (capteur binaire)"""
        data = payload.get('data', 0)
        
        logger.debug(f"1BS Data: {data:02x}")
    
    async def stop(self):
        """Arrêter le pont"""
        self.running = False
        logger.info("Pont Home Assistant arrêté")
