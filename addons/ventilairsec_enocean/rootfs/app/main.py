#!/usr/bin/env python3
"""
Addon Home Assistant - Support Ventilairsec Enocean
Permet la communication avec VMI Purevent via protocole Enocean
"""

import logging
import sys
import os
import json
import asyncio
import threading
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('ventilairsec_enocean')

# Importer les modules locaux
sys.path.insert(0, '/app/enocean')
sys.path.insert(0, '/app')

from enocean_daemon import EnoceanDaemon
from homeassistant_bridge import HomeAssistantBridge

class VentilairsecAddon:
    """Classe principale pour l'addon Ventilairsec"""
    
    def __init__(self):
        """Initialiser l'addon"""
        self.daemon = None
        self.bridge = None
        self.config = self.load_config()
        
    def load_config(self):
        """Charger la configuration depuis le fichier ini"""
        config_path = Path('/etc/ventilairsec/config.ini')
        config = {
            'enocean': {
                'serial_port': '/dev/ttyUSB0',
                'serial_rate': 115200,
                'socket_port': 55006,
                'cycle_time': 0.3,
                'debug_logging': False
            },
            'homeassistant': {
                'host': 'supervisor',
                'port': 8123,
            }
        }
        
        if config_path.exists():
            import configparser
            ini = configparser.ConfigParser()
            ini.read(config_path)
            
            if 'enocean' in ini:
                config['enocean'].update(dict(ini['enocean']))
            if 'homeassistant' in ini:
                config['homeassistant'].update(dict(ini['homeassistant']))
        
        logger.info(f"Configuration chargée: {config}")
        return config
    
    async def start(self):
        """Démarrer l'addon"""
        logger.info("=== Démarrage de l'addon Ventilairsec Enocean ===")
        
        try:
            # Initialiser le daemon Enocean
            enocean_config = self.config.get('enocean', {})
            self.daemon = EnoceanDaemon(enocean_config)
            
            logger.info("Initialisation du daemon Enocean...")
            await self.daemon.initialize()
            
            # Initialiser le pont Home Assistant
            ha_config = self.config.get('homeassistant', {})
            self.bridge = HomeAssistantBridge(ha_config, self.daemon)
            
            logger.info("Initialisation du pont Home Assistant...")
            await self.bridge.initialize()
            
            # Lancer les threads
            daemon_thread = threading.Thread(target=self.daemon.run, daemon=True)
            daemon_thread.start()
            logger.info("Daemon Enocean lancé")
            
            bridge_thread = threading.Thread(target=self.bridge.run, daemon=True)
            bridge_thread.start()
            logger.info("Pont Home Assistant lancé")
            
            # Garder le programme actif
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Arrêt demandé par l'utilisateur")
            await self.stop()
        except Exception as e:
            logger.error(f"Erreur lors du démarrage: {e}", exc_info=True)
            await self.stop()
            sys.exit(1)
    
    async def stop(self):
        """Arrêter l'addon"""
        logger.info("Arrêt de l'addon...")
        
        if self.daemon:
            self.daemon.stop()
        if self.bridge:
            await self.bridge.stop()
        
        logger.info("Addon arrêté")

async def main():
    """Point d'entrée principal"""
    addon = VentilairsecAddon()
    await addon.start()

if __name__ == '__main__':
    asyncio.run(main())
