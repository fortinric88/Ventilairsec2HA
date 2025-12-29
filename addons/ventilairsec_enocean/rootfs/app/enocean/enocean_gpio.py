"""
Communication GPIO pour EnOcean Pi - Module Enocean sur GPIO Raspberry Pi
"""

import logging
import time
from typing import Callable, Optional, Dict, Any
from queue import Queue

try:
    import board
    import busio
    HAS_BOARD = True
except ImportError:
    HAS_BOARD = False

try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False

logger = logging.getLogger('ventilairsec_enocean.gpio')


class EnoceanGPIOBridge:
    """Bridge pour communiquer avec EnOcean Pi via GPIO (SPI/UART)"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialiser le bridge GPIO Enocean
        
        Args:
            config: Dictionnaire contenant:
                - communication_mode: "gpio" ou "serial"
                - gpio_mode: "spi", "uart" ou "i2c" (si GPIO)
                - gpio_tx_pin: Pin GPIO pour TX (UART) ou CS (SPI)
                - gpio_rx_pin: Pin GPIO pour RX (UART)
                - gpio_reset_pin: Pin GPIO pour RESET (optionnel)
                - debug_logging: Activer les logs détaillés
        """
        self.config = config
        self.running = False
        self.spi = None
        self.receive_queue = Queue()
        self.listeners = []
        
        # Déterminer le mode GPIO
        self.gpio_mode = config.get('gpio_mode', 'spi')
        self.tx_pin = config.get('gpio_tx_pin', 24)  # GPIO24 par défaut
        self.rx_pin = config.get('gpio_rx_pin', 25)  # GPIO25 par défaut
        self.reset_pin = config.get('gpio_reset_pin', 17)  # GPIO17 pour RESET
        
        logger.info(f"GPIO Bridge initialized (mode={self.gpio_mode}, TX={self.tx_pin}, RX={self.rx_pin})")
    
    async def initialize(self):
        """Initialiser la communication GPIO"""
        try:
            if self.gpio_mode == 'spi':
                await self._init_spi()
            elif self.gpio_mode == 'uart':
                await self._init_uart()
            elif self.gpio_mode == 'i2c':
                await self._init_i2c()
            else:
                raise ValueError(f"Mode GPIO inconnu: {self.gpio_mode}")
                
            logger.info(f"GPIO communication initialized ({self.gpio_mode})")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation GPIO: {e}")
            raise
    
    async def _init_spi(self):
        """Initialiser la communication SPI"""
        if not HAS_BOARD:
            raise ImportError("Module 'board' non disponible. Installez Adafruit libraries.")
        
        import digitalio
        
        try:
            # SPI sur pins GPIO
            self.spi = busio.SPI(
                clock=board.SCK,      # GPIO11
                MOSI=board.MOSI,      # GPIO10
                MISO=board.MISO       # GPIO9
            )
            
            # Chip select
            self.cs = digitalio.DigitalInOut(board.D24)  # GPIO24
            self.cs.direction = digitalio.Direction.OUTPUT
            self.cs.value = True
            
            logger.info("SPI initialized (clock=GPIO11, MOSI=GPIO10, MISO=GPIO9, CS=GPIO24)")
            
        except Exception as e:
            logger.error(f"Erreur SPI: {e}")
            raise
    
    async def _init_uart(self):
        """Initialiser la communication UART sur GPIO"""
        if not HAS_GPIO:
            raise ImportError("Module RPi.GPIO non disponible. Installez RPi.GPIO.")
        
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.tx_pin, GPIO.OUT)
            GPIO.setup(self.rx_pin, GPIO.IN)
            
            if self.reset_pin:
                GPIO.setup(self.reset_pin, GPIO.OUT)
                GPIO.output(self.reset_pin, GPIO.HIGH)
            
            logger.info(f"UART GPIO initialized (TX={self.tx_pin}, RX={self.rx_pin})")
            
        except Exception as e:
            logger.error(f"Erreur UART GPIO: {e}")
            raise
    
    async def _init_i2c(self):
        """Initialiser la communication I2C"""
        if not HAS_BOARD:
            raise ImportError("Module 'board' non disponible. Installez Adafruit libraries.")
        
        try:
            self.i2c = busio.I2C(board.SCL, board.SDA)
            logger.info("I2C initialized (SCL=GPIO3, SDA=GPIO2)")
            
        except Exception as e:
            logger.error(f"Erreur I2C: {e}")
            raise
    
    async def read_packet(self) -> Optional[bytes]:
        """Lire un paquet Enocean via GPIO"""
        try:
            if self.gpio_mode == 'spi':
                return await self._read_spi()
            elif self.gpio_mode == 'uart':
                return await self._read_uart()
            elif self.gpio_mode == 'i2c':
                return await self._read_i2c()
        except Exception as e:
            logger.error(f"Erreur lecture GPIO: {e}")
            return None
    
    async def _read_spi(self) -> Optional[bytes]:
        """Lire via SPI"""
        try:
            # Lire 1 octet (status/length)
            self.cs.value = False
            time.sleep(0.001)
            
            status = bytearray(1)
            self.spi.readinto(status)
            
            self.cs.value = True
            
            if status[0] == 0:
                return None
            
            # Lire le reste du paquet
            length = status[0] & 0x7F
            
            self.cs.value = False
            time.sleep(0.001)
            
            packet = bytearray(length)
            self.spi.readinto(packet)
            
            self.cs.value = True
            
            return bytes(packet)
            
        except Exception as e:
            logger.error(f"Erreur SPI read: {e}")
            return None
    
    async def _read_uart(self) -> Optional[bytes]:
        """Lire via UART GPIO (simulation)"""
        try:
            # Note: La vraie lecture UART nécessite une UART virtuelle
            # ou une implémentation software-bitbanged complexe
            logger.warning("UART GPIO read not fully implemented, returning None")
            return None
            
        except Exception as e:
            logger.error(f"Erreur UART read: {e}")
            return None
    
    async def _read_i2c(self) -> Optional[bytes]:
        """Lire via I2C"""
        try:
            # Adresse I2C standard du TCM Enocean: 0x80
            address = 0x80
            
            # Lire le header (2 bytes)
            header = bytearray(2)
            try:
                self.i2c.readfrom_into(address, header)
            except:
                return None
            
            if header[0] == 0:
                return None
            
            length = header[0]
            
            # Lire le reste
            packet = bytearray(length - 2)
            try:
                self.i2c.readfrom_into(address, packet)
            except:
                return None
            
            return bytes(header + packet)
            
        except Exception as e:
            logger.error(f"Erreur I2C read: {e}")
            return None
    
    async def write_packet(self, packet: bytes) -> bool:
        """Envoyer un paquet Enocean via GPIO"""
        try:
            if self.gpio_mode == 'spi':
                return await self._write_spi(packet)
            elif self.gpio_mode == 'i2c':
                return await self._write_i2c(packet)
            else:
                logger.warning(f"Write not supported for {self.gpio_mode}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur write GPIO: {e}")
            return False
    
    async def _write_spi(self, packet: bytes) -> bool:
        """Écrire via SPI"""
        try:
            self.cs.value = False
            time.sleep(0.001)
            
            self.spi.write(packet)
            
            time.sleep(0.001)
            self.cs.value = True
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur SPI write: {e}")
            return False
    
    async def _write_i2c(self, packet: bytes) -> bool:
        """Écrire via I2C"""
        try:
            address = 0x80
            self.i2c.writeto(address, packet)
            return True
            
        except Exception as e:
            logger.error(f"Erreur I2C write: {e}")
            return False
    
    def add_listener(self, callback: Callable):
        """Ajouter un listener pour les paquets reçus"""
        self.listeners.append(callback)
    
    def shutdown(self):
        """Arrêter la communication GPIO"""
        try:
            if HAS_GPIO:
                GPIO.cleanup()
            self.running = False
            logger.info("GPIO bridge shutdown")
        except Exception as e:
            logger.error(f"Erreur shutdown: {e}")
