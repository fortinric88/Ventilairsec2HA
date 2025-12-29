# Addon Ventilairsec Enocean pour Home Assistant

Support pour VMI Purevent Ventilairsec via le protocole de communication Enocean.

## Description

Cet addon permet à Home Assistant de communiquer avec les systèmes de ventilation Ventilairsec (VMI Purevent) en utilisant le protocole Enocean. Il agit comme passerelle entre les appareils Enocean sans fil et Home Assistant.

### Fonctionnalités

- ✅ Communication directe via USB Enocean (TCM310, RPI Enocean, etc.)
- ✅ Découverte automatique des appareils
- ✅ Support des capteurs de température/humidité
- ✅ Support des commandes de ventilation
- ✅ Historique des appareils découverts
- ✅ Logs de débogage détaillés
- ✅ Reconnexion automatique

### Appareils supportés

- **VMI Purevent D1079-01-00** : Thermostat/ventilateur intelligent
- **Capteurs 4BS (A5-20-01)** : Température, humidité
- **Capteurs 1BS (D5)** : Contacteurs, boutons sans fil
- **Autres appareils Enocean** : Avec décodage générique

## Installation

### Prérequis

1. **Home Assistant** : Version 2023.1 ou supérieure
2. **Dongle Enocean USB** : 
   - TCM310 (recommandé)
   - RPI Enocean
   - Autres modules Enocean compatibles
3. **Port USB libre** sur votre serveur Home Assistant

### Installation du Store

1. Accédez à **Paramètres → Modules complémentaires → Créer et gérer**
2. Ajoutez ce dépôt : `https://github.com/fortinric88/Ventilairsec2HA`
3. Cherchez "Ventilairsec Enocean"
4. Cliquez sur **Installer**

### Installation manuelle

1. Clonez le dépôt dans le répertoire addons :
```bash
cd /config/addons
git clone https://github.com/fortinric88/Ventilairsec2HA
cd Ventilairsec2HA
```

2. Redémarrez Home Assistant
3. Accédez à **Paramètres → Modules complémentaires**
4. Installez l'addon Ventilairsec Enocean

## Configuration

### Paramètres de base

Accédez aux **Options** de l'addon :

| Paramètre | Défaut | Description |
|-----------|--------|-------------|
| **Port série** | `/dev/ttyUSB0` | Port du dongle USB Enocean |
| **Vitesse (baud)** | `115200` | Vitesse de communication |
| **Port socket** | `55006` | Port TCP interne |
| **Cycle (s)** | `0.3` | Temps de cycle de traitement |
| **Debug** | Non | Activer les logs détaillés |

### Détection du port

Pour identifier votre port Enocean :

```bash
# Sur le serveur Home Assistant
ls -la /dev/tty*
```

Regardez pour :
- `/dev/ttyUSB0` ou `/dev/ttyUSB1` (USB)
- `/dev/ttyACM0` (USB CDC)
- `/dev/ttyAMA0` (GPIO sur Raspberry Pi)

## Utilisation

### Découverte d'appareils

Une fois l'addon lancé, les appareils Enocean sont découverts automatiquement :

1. Les appareils sont listés dans les **Appareil et Services**
2. Cliquez sur chaque appareil pour voir les entités
3. Ajoutez les entités à votre interface Home Assistant

### Intégration avec les automatisations

Exemple : Augmenter la ventilation si l'humidité dépasse 60%

```yaml
automation:
  - alias: "Augmenter ventilation humidité élevée"
    trigger:
      platform: numeric_state
      entity_id: sensor.ventilairsec_humidity
      above: 60
    action:
      service: fan.set_percentage
      data:
        entity_id: fan.ventilairsec_fan
        percentage: 80
```

### Cartes Lovelace

```yaml
type: entities
title: Ventilairsec
entities:
  - sensor.ventilairsec_temperature
  - sensor.ventilairsec_humidity
  - fan.ventilairsec_fan
```

## Dépannage

### L'addon ne démarre pas

1. Vérifiez que le **port série est correct**
2. Consultez les **logs** (bouton Logs dans l'interface addon)
3. Essayez en mettant **Debug: On**

### Pas d'appareils découverts

1. Vérifiez que le **dongle Enocean est en mode de réception**
2. Activez le **mode d'appairage** sur vos appareils Ventilairsec
3. Attendez 30-60 secondes pour la découverte

### Perte de connexion

L'addon tente de se reconnecter automatiquement :

1. Vérifiez la **stabilité du port USB**
2. Vérifiez les **interférences radio** (2.4 GHz)
3. Redémarrez l'addon

## Logs et débogage

### Activer les logs détaillés

1. Allez aux **Options**
2. Activez **Debug logging**
3. Redémarrez l'addon
4. Consultez les **Logs**

### Sauvegarder les logs

```
Les logs sont disponibles à :
/config/addons/ventilairsec_enocean/logs/
```

## Développement

### Structure du projet

```
addons/ventilairsec_enocean/
├── addon.yaml              # Configuration de l'addon
├── Dockerfile              # Image Docker
├── requirements.txt        # Dépendances Python
├── rootfs/
│   ├── run.sh             # Script de démarrage
│   ├── etc/
│   │   └── cont-init.d/   # Scripts d'initialisation
│   └── app/
│       ├── main.py        # Point d'entrée
│       ├── enocean/
│       │   └── enocean_daemon.py  # Daemon de communication
│       ├── homeassistant_bridge.py # Passerelle HA
│       ├── homeassistant_entities.py # Entités HA
│       └── device_config.py # Configuration des appareils
└── README.md              # Ce fichier
```

### Contribuer

Les contributions sont bienvenues ! Pour contribuer :

1. Forkez le dépôt
2. Créez une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements
4. Poussez vers la branche
5. Créez une Pull Request

## Licence

GPL-3.0 License - Voir LICENSE pour les détails

## Support

Pour les problèmes et suggestions :

- **Issues** : https://github.com/fortinric88/Ventilairsec2HA/issues
- **Discussions** : https://github.com/fortinric88/Ventilairsec2HA/discussions

## Ressources

- [Documentation Enocean](https://www.enocean.com/en/)
- [Forum Home Assistant](https://community.home-assistant.io/)
- [Ventilairsec](https://www.ventilairsec.com/)
