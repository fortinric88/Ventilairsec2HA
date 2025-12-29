# Guide de Contribution

Merci de vouloir contribuer à Ventilairsec Home Assistant! 🎉

Ce guide explique comment contribuer au projet.

## Avant de commencer

Lisez :
- [README.md](../README.md) - Vue d'ensemble du projet
- [Code of Conduct](#code-of-conduct) - Règles de conduite

## Types de contributions

### 1. Signaler des bugs 🐛

**Créez une issue** avec :

- **Titre clair** : "L'addon refuse de démarrer"
- **Environnement** :
  ```
  - Home Assistant : 2024.1.0
  - Addon : 1.0.0
  - Dongle : TCM 310
  - Système : Raspberry Pi 4
  ```
- **Reproduction** :
  ```
  1. Connectez le dongle
  2. Configurez le port
  3. Démarrez l'addon
  4. ERROR: Port not found
  ```
- **Logs** : Copiez les 30 dernières lignes (en mode debug)
- **Comportement attendu** : Ce que devrait faire l'addon

### 2. Proposer des améliorations 💡

**Créez une discussion** ou une issue avec :

- **Description** : Qu'est-ce que vous voulez ajouter?
- **Cas d'usage** : Pourquoi c'est important
- **Implémentation** : Comment vous le voyez
- **Alternatives** : Autres approches possibles

Exemples :
- Support de nouveaux appareils Enocean
- Interface web pour configuration
- Intégration MQTT
- Statistiques et graphiques

### 3. Améliorer la documentation 📖

**Pull Request directe** pour :

- Corriger des typos
- Clarifier les instructions
- Ajouter des exemples
- Traduire en autre langue

### 4. Contribuer du code 💻

Voir [Processus de contribution code](#processus-de-contribution-code)

## Processus de contribution code

### Étape 1 : Préparez votre environnement

```bash
# Clonez le dépôt
git clone https://github.com/fortinric88/Ventilairsec2HA.git
cd Ventilairsec2HA

# Créez une branche
git checkout -b feature/description-courte
# Ou pour un bug :
git checkout -b fix/description-courte
```

### Étape 2 : Développez votre changement

**Structure du code** :

```
addons/ventilairsec_enocean/rootfs/app/
├── main.py                    # Entrée
├── enocean_daemon.py         # Protocole Enocean
├── homeassistant_bridge.py   # Intégration HA
├── homeassistant_entities.py # Entités HA
└── device_config.py          # Profils d'appareils
```

**Conventions de code** :

```python
# PEP 8 - Formatage standard Python
# - 4 espaces d'indentation
# - Noms en snake_case
# - Commentaires clairs
# - Docstrings pour les fonctions publiques

def process_radio_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    """
    Traiter un paquet radio Enocean.
    
    Args:
        packet: Dictionnaire du paquet
        
    Returns:
        Données parses du paquet
    """
    # Votre code
    pass
```

**Tests** :

```bash
# Testez localement
docker-compose -f docker-compose.dev.yml up

# Vérifiez les logs
docker logs ventilairsec_enocean

# Testez vos changements
# - Démarrage de l'addon
# - Découverte d'appareils
# - Recepton de données
```

### Étape 3 : Commiter vos changements

```bash
# Vérifiez les modifications
git status
git diff

# Stagez les fichiers
git add chemin/vers/fichier.py

# Committez avec un message clair
git commit -m "Fix: Corriger erreur CRC dans enocean_daemon.py

- Description du problème
- Comment c'était cassé
- Comment c'est fixé
- Vérifié avec test XYZ
"
```

**Messages de commit** :

```
[type]([scope]): Description courte

Description longue...

Fixes #123           # Si ça ferme une issue
Related to #456      # Si c'est lié
```

Types autorisés :
- `feat` - Nouvelle fonctionnalité
- `fix` - Correction de bug
- `docs` - Documentation
- `test` - Tests
- `refactor` - Refonte
- `style` - Formatage
- `perf` - Performance
- `chore` - Maintenance

### Étape 4 : Pushez et créez une Pull Request

```bash
# Poussez votre branche
git push origin feature/description-courte

# Allez sur GitHub
# Une bannière invite à créer une PR
# Cliquez "Compare & pull request"
```

**Template PR** :

```markdown
## Description
Courte description de ce que cette PR fait

## Lié à
- Fixes #123
- Related to #456

## Type de changement
- [x] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Checklist
- [ ] Mon code suit les conventions du projet
- [ ] J'ai documenté mes changements
- [ ] J'ai testé localement
- [ ] Pas de warnings ou erreurs
- [ ] Les tests passent

## Screenshots (optionnel)
Si pertinent, ajoutez des screenshots
```

### Étape 5 : Répondez aux reviews

Les mainteneurs vont :
- Lire votre code
- Faire des suggestions
- Demander des clarifications

**Répondez professionnellement** :

```
Merci pour la review! 

J'ai changé X comme suggéré.
Pour Y, j'ai fait Z car...

🔄 Pushé les changements
```

## Support d'un nouvel appareil

Si vous voulez ajouter le support d'un appareil :

### 1. Créez une issue

```
Title: Support de [Appareil XXX]

- ID Enocean : A5F12345
- Profil RORG : 0xA5 (4BS)
- Données : Température, Humidité, Vitesse fan
- Spec : [lien vers doc]
```

### 2. Développez le profil

Exemple pour un nouveau capteur :

```python
# Dans device_config.py

'A5-99-99': {
    'name': 'Mon nouveau capteur',
    'rorg': 0xA5,
    'entities': {
        'temperature': {
            'type': 'temperature',
            'name': 'Température',
            'unit': '°C',
            'byte': 1,
            'scale_min': -40,
            'scale_max': 62
        },
        'humidity': {
            'type': 'humidity',
            'name': 'Humidité',
            'unit': '%',
            'byte': 2,
            'scale_min': 0,
            'scale_max': 100
        }
    }
}
```

### 3. Testez

```bash
# Testez la découverte
# Testez le parsing des données
# Vérifiez les valeurs
```

### 4. Créez une PR

Incluez :
- Le profil dans `device_config.py`
- Docs dans `DEVICES.md`
- Tests

## Standards de code

### Python

- **PEP 8** - Style standard
- **Type hints** - Utilisez les types
- **Docstrings** - Documentez publiquement
- **Tests** - Couvrez vos changements
- **Logs** - Utilisez le logging standard

Exemple :

```python
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class MyClass:
    """Description de ma classe."""
    
    def process(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Traiter les données.
        
        Args:
            data: Dictionnaire à traiter
            
        Returns:
            Résultat traité ou None si erreur
            
        Raises:
            ValueError: Si les données sont invalides
        """
        try:
            result = self._internal_process(data)
            logger.info(f"Résultat: {result}")
            return result
        except Exception as e:
            logger.error(f"Erreur: {e}", exc_info=True)
            return None
    
    def _internal_process(self, data: Dict[str, Any]) -> str:
        """Traitement interne."""
        # ...
        pass
```

### YAML/Configuration

- 2 espaces d'indentation
- Commentaires clairs
- Clés lisibles

```yaml
# Bon
serial_port: /dev/ttyUSB0
serial_rate: 115200

# Mauvais
port: /dev/ttyUSB0
rate: 115200
```

## Tests

### Exécuter les tests

```bash
# Tests Python
python -m pytest tests/

# Tests d'intégration
docker-compose -f docker-compose.test.yml up
```

### Écrire des tests

```python
# tests/test_enocean_daemon.py

import pytest
from app.enocean_daemon import EnoceanDaemon

def test_crc_verification():
    """Vérifier le calcul CRC."""
    daemon = EnoceanDaemon({})
    
    # Test correct
    assert daemon._verify_crc(0x01, b'\x12\x34', 0x37)
    
    # Test mauvais
    assert not daemon._verify_crc(0x01, b'\x12\x34', 0xFF)
```

## Documentation

### Structure

```
docs/
├── DEVICES.md           # Appareils supportés
├── FAQ.md              # Questions fréquentes
├── ARCHITECTURE.md     # Architecture
├── ENOCEAN_PROTOCOL.md # Spécifications
└── ADVANCED.md         # Configuration avancée
```

### Écrire de la documentation

- **Clair et concis** - Évitez le jargon
- **Exemples** - Montrez comment utiliser
- **Code** - Formattez correctement
- **Liens** - Liez vers d'autres docs

## Code of Conduct

### Soyez respectueux

- 🤝 Traitez les autres avec respect
- 💬 Écoutez les autres perspectives
- 🚫 Pas de harcèlement, discrimination
- 📛 Reportez les problèmes aux modérateurs

### Participez de bonne foi

- ✅ Faites des contributions réfléchies
- 📚 Lisez avant de commenter
- 🎯 Restez focus sur le code
- 🤐 Gardez les secrets

## Merci! 🙏

Chaque contribution, peu importe sa taille, aide le projet.

Questions? Créez une discussion : https://github.com/fortinric88/Ventilairsec2HA/discussions

---

**Auteur** : fortinric88  
**Licence** : GNU General Public License v3.0
