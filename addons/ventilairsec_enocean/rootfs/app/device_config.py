"""
Configuration des appareils Ventilairsec
"""

# Mappage des IDs RORG vers les types d'appareils
RORG_MAPPING = {
    0xA5: {
        'name': '4-byte Communication (4BS)',
        'description': 'Données 4 octets - généralement pour capteurs thermiques',
        'data_length': 4
    },
    0xD5: {
        'name': '1-byte Communication (1BS)',
        'description': 'Données 1 octet - généralement pour capteurs simples',
        'data_length': 1
    },
    0xD2: {
        'name': 'Variable Length Communication (VLD)',
        'description': 'Données de longueur variable',
        'data_length': None
    }
}

# Profils d'appareils Ventilairsec connus
DEVICE_PROFILES = {
    'D1079-01-00': {
        'name': 'VMI Purevent D1079-01-00',
        'rorg': 0xA5,
        'entities': {
            'temperature': {
                'type': 'temperature',
                'name': 'Température',
                'unit': '°C'
            },
            'humidity': {
                'type': 'humidity',
                'name': 'Humidité',
                'unit': '%'
            },
            'fan_speed': {
                'type': 'fan',
                'name': 'Vitesse ventilation',
                'unit': '%'
            }
        }
    },
    'A5-20-01': {
        'name': 'Capteur Température/Humidité 4BS',
        'rorg': 0xA5,
        'entities': {
            'temperature': {
                'type': 'temperature',
                'name': 'Température',
                'unit': '°C'
            },
            'humidity': {
                'type': 'humidity',
                'name': 'Humidité',
                'unit': '%'
            }
        }
    },
    'D5-00-01': {
        'name': 'Capteur de Contact',
        'rorg': 0xD5,
        'entities': {
            'contact': {
                'type': 'binary_sensor',
                'name': 'Contact',
                'device_class': 'door'
            }
        }
    }
}

# Paramètres de décodage pour A5-20-01 (4BS commun)
A5_20_01_DECODER = {
    'temperature': {
        'byte': 1,
        'bit_from': 0,
        'bit_to': 7,
        'scale_min': -40,
        'scale_max': 62,
        'description': 'Température linéaire'
    },
    'humidity': {
        'byte': 2,
        'bit_from': 0,
        'bit_to': 7,
        'scale_min': 0,
        'scale_max': 100,
        'description': 'Humidité relative'
    }
}

# Paramètres pour D1079-01-00 (VMI Purevent)
D1079_DECODER = {
    'temperature': {
        'bytes': [1, 2],
        'scale_min': -40,
        'scale_max': 62,
        'description': 'Température'
    },
    'humidity': {
        'byte': 3,
        'scale_min': 0,
        'scale_max': 100,
        'description': 'Humidité'
    },
    'fan_speed': {
        'byte': 0,
        'scale_min': 0,
        'scale_max': 255,
        'description': 'Vitesse du ventilateur (0-255)'
    }
}


def get_device_profile(device_type: str) -> dict:
    """Récupérer le profil d'un appareil"""
    return DEVICE_PROFILES.get(device_type, {})


def decode_4bs_data(data: bytes, decoder: dict) -> dict:
    """Décoder les données 4BS selon le décodeur fourni"""
    result = {}
    
    for key, config in decoder.items():
        byte_idx = config.get('byte', 0)
        if byte_idx < len(data):
            value = data[byte_idx]
            scale_min = config.get('scale_min', 0)
            scale_max = config.get('scale_max', 255)
            
            # Normaliser la valeur
            normalized = (value / 255.0) * (scale_max - scale_min) + scale_min
            result[key] = round(normalized, 2)
    
    return result
