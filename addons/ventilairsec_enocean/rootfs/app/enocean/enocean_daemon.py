"""
Daemon Enocean - Gère la communication via le port série avec les appareils Enocean
"""

import logging
import serial
import threading
import time
import struct
from typing import Callable, Optional, Dict, Any
from queue import Queue

logger = logging.getLogger('ventilairsec_enocean.daemon')

class EnoceanDaemon:
    """Daemon pour gérer la communication Enocean"""
    
    # Constantes Enocean
    ENOCEAN_HEADER = 0x55
    ENOCEAN_SYNC_BYTE = 0x55
    
    # Types de paquets
    PACKET_TYPE_RESERVED = 0
    PACKET_TYPE_RADIO = 1
    PACKET_TYPE_RESPONSE = 2
    PACKET_TYPE_RADIO_SUB_TEL = 3
    PACKET_TYPE_EVENT = 4
    PACKET_TYPE_COMMON_COMMAND = 5
    PACKET_TYPE_SMART_ACK_COMMAND = 6
    PACKET_TYPE_REMOTE_MAN_COMMAND = 7
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialiser le daemon Enocean
        
        Args:
            config: Dictionnaire de configuration contenant:
                - serial_port: Port série (ex: /dev/ttyUSB0)
                - serial_rate: Vitesse (ex: 115200)
                - socket_port: Port de socket interne
                - cycle_time: Temps de cycle de traitement
                - debug_logging: Activer les logs détaillés
        """
        self.config = config
        self.serial = None
        self.running = False
        self.receive_queue = Queue()
        self.send_queue = Queue()
        self.listeners = []
        
    async def initialize(self):
        """Initialiser la connexion série"""
        try:
            port = self.config.get('serial_port', '/dev/ttyUSB0')
            rate = int(self.config.get('serial_rate', 115200))
            
            logger.info(f"Initialisation du port série {port} @ {rate} baud...")
            
            self.serial = serial.Serial(
                port=port,
                baudrate=rate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1.0
            )
            
            if self.serial.is_open:
                logger.info("Port série ouvert avec succès")
                # Vider le buffer
                self.serial.reset_input_buffer()
                self.serial.reset_output_buffer()
            else:
                raise RuntimeError(f"Impossible d'ouvrir le port {port}")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du port série: {e}")
            raise
    
    def run(self):
        """Lancer le daemon de lecture/écriture"""
        self.running = True
        logger.info("Daemon Enocean démarré")
        
        while self.running:
            try:
                self._process_receive()
                self._process_send()
                time.sleep(0.01)
            except Exception as e:
                logger.error(f"Erreur dans le daemon: {e}")
    
    def _process_receive(self):
        """Traiter les données reçues du port série"""
        if not self.serial or not self.serial.is_open:
            return
        
        if self.serial.in_waiting > 0:
            try:
                byte = self.serial.read(1)
                if byte and byte[0] == self.ENOCEAN_SYNC_BYTE:
                    packet = self._read_packet()
                    if packet:
                        self._handle_packet(packet)
            except Exception as e:
                logger.error(f"Erreur lors de la réception: {e}")
    
    def _read_packet(self) -> Optional[Dict[str, Any]]:
        """Lire un paquet Enocean complet"""
        try:
            # Lire header: [SYNC][LENGTH_H][LENGTH_L][TYPE]
            header = self.serial.read(4)
            if len(header) < 4:
                return None
            
            sync, length_h, length_l, ptype = header
            
            if sync != self.ENOCEAN_SYNC_BYTE:
                logger.warning(f"Byte de synchronisation invalide: {sync:02x}")
                return None
            
            data_len = (length_h << 8) | length_l
            
            # Lire les données et le CRC
            data = self.serial.read(data_len + 1)
            if len(data) < data_len + 1:
                logger.warning("Données incomplet")
                return None
            
            payload = data[:-1]
            crc = data[-1]
            
            # Vérifier le CRC
            if not self._verify_crc(ptype, payload, crc):
                logger.warning("Erreur CRC détectée")
                return None
            
            packet = {
                'type': ptype,
                'length': data_len,
                'data': payload,
                'crc': crc
            }
            
            logger.debug(f"Paquet reçu: type={ptype}, len={data_len}")
            return packet
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du paquet: {e}")
            return None
    
    def _verify_crc(self, ptype: int, data: bytes, crc: int) -> bool:
        """Vérifier le CRC d'un paquet"""
        # Calcul CRC8
        calculated = ptype
        for byte in data:
            calculated ^= byte
        return calculated == crc
    
    def _process_send(self):
        """Traiter l'envoi de données"""
        if not self.send_queue.empty() and self.serial and self.serial.is_open:
            try:
                packet = self.send_queue.get_nowait()
                self._send_packet(packet)
            except:
                pass
    
    def _send_packet(self, packet: Dict[str, Any]):
        """Envoyer un paquet Enocean"""
        try:
            ptype = packet.get('type', self.PACKET_TYPE_RADIO)
            data = packet.get('data', b'')
            
            # Construire le paquet
            length = len(data)
            length_h = (length >> 8) & 0xFF
            length_l = length & 0xFF
            
            # Calculer le CRC
            crc = ptype
            for byte in data:
                crc ^= byte
            
            # Envoyer: [SYNC][LENGTH_H][LENGTH_L][TYPE][DATA][CRC]
            frame = bytes([
                self.ENOCEAN_SYNC_BYTE,
                length_h,
                length_l,
                ptype
            ]) + data + bytes([crc])
            
            self.serial.write(frame)
            logger.debug(f"Paquet envoyé: type={ptype}, len={length}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi: {e}")
    
    def _handle_packet(self, packet: Dict[str, Any]):
        """Traiter un paquet reçu"""
        ptype = packet.get('type')
        
        if ptype == self.PACKET_TYPE_RADIO:
            self._handle_radio_packet(packet)
        elif ptype == self.PACKET_TYPE_RESPONSE:
            logger.debug("Paquet de réponse reçu")
        elif ptype == self.PACKET_TYPE_EVENT:
            self._handle_event(packet)
        else:
            logger.debug(f"Paquet de type inconnu: {ptype}")
        
        # Notifier les listeners
        for listener in self.listeners:
            try:
                listener(packet)
            except Exception as e:
                logger.error(f"Erreur dans le listener: {e}")
    
    def _handle_radio_packet(self, packet: Dict[str, Any]):
        """Traiter un paquet radio (données d'appareils)"""
        data = packet.get('data', b'')
        if len(data) < 7:
            return
        
        # Format: [RORG][DATA...][SENDER_ID...][STATUS]
        rorg = data[0]
        payload = data[1:-5]
        sender_id = int.from_bytes(data[-5:-1], 'big')
        status = data[-1]
        
        logger.debug(f"Paquet radio: RORG={rorg:02x}, ID={sender_id:08x}, Status={status:02x}")
        
        # Parser les données selon le type RORG
        parsed = self._parse_radio_payload(rorg, payload)
        
        event = {
            'type': 'radio_message',
            'rorg': rorg,
            'sender_id': sender_id,
            'status': status,
            'payload': parsed
        }
        
        self.receive_queue.put(event)
    
    def _handle_event(self, packet: Dict[str, Any]):
        """Traiter un événement système Enocean"""
        data = packet.get('data', b'')
        if len(data) < 1:
            return
        
        event_code = data[0]
        logger.info(f"Événement Enocean: code={event_code:02x}")
    
    def _parse_radio_payload(self, rorg: int, payload: bytes) -> Dict[str, Any]:
        """Parser les données selon le type RORG"""
        parsed = {
            'rorg': rorg,
            'raw': payload.hex()
        }
        
        # A5 - 4BS (4 bytes)
        if rorg == 0xA5:
            if len(payload) >= 4:
                parsed['type'] = '4BS'
                parsed['db3'] = payload[0]
                parsed['db2'] = payload[1]
                parsed['db1'] = payload[2]
                parsed['db0'] = payload[3]
        
        # D5 - 1BS (1 byte)
        elif rorg == 0xD5:
            if len(payload) >= 1:
                parsed['type'] = '1BS'
                parsed['data'] = payload[0]
        
        # D2 - Variable (variable)
        elif rorg == 0xD2:
            parsed['type'] = 'VAR'
            parsed['data'] = payload.hex()
        
        return parsed
    
    def add_listener(self, callback: Callable):
        """Ajouter un listener pour les paquets reçus"""
        self.listeners.append(callback)
    
    def send_packet(self, packet: Dict[str, Any]):
        """Ajouter un paquet à envoyer"""
        self.send_queue.put(packet)
    
    def get_received_packet(self) -> Optional[Dict[str, Any]]:
        """Récupérer un paquet reçu"""
        try:
            return self.receive_queue.get_nowait()
        except:
            return None
    
    def stop(self):
        """Arrêter le daemon"""
        self.running = False
        if self.serial and self.serial.is_open:
            self.serial.close()
        logger.info("Daemon Enocean arrêté")
