# Ventilairsec Home Assistant 🏠🌬️

Addon Home Assistant pour supporter la **VMI Purevent Ventilairsec** et les appareils Enocean via le protocole de communication **EnOcean**.

## Vue d'ensemble

Cet addon permet à Home Assistant de communiquer directement avec les systèmes de ventilation contrôlée Ventilairsec et les capteurs Enocean.

### Fonctionnalités principales

✅ **Communication Enocean** - Support complet du protocole 4BS et 1BS  
✅ **Découverte automatique** - Les appareils Enocean sont automatiquement détectés  
✅ **Intégration Home Assistant** - Capteurs et commandes natifs  
✅ **Contrôle VMI** - Gestion de la ventilation (vitesse, modes)  
✅ **Monitoring** - Température, humidité, état du système  

## Démarrage rapide

### 1. Prérequis

- Home Assistant 2024.1+
- Dongle Enocean USB (TCM 310, TCM 320, etc.)
- VMI Purevent Ventilairsec (optionnel, pour la ventilation)

### 2. Installation

**Méthode recommandée (via dépôt)** :

1. Ouvrez Home Assistant
2. **Paramètres** → **Modules complémentaires** → ⋮ (trois points)
3. **Dépôts**
4. Entrez : `https://github.com/fortinric88/Ventilairsec2HA`
5. Cliquez **Créer**
6. Cherchez "Ventilairsec Enocean" et cliquez **Installer**

**Plus de détails** : Voir [INSTALL.md](./INSTALL.md)

### 3. Configuration

Une fois installé :

1. **Dépôts** → **Ventilairsec Enocean** → **Options**
2. Sélectionnez le port série de votre dongle USB
3. Cliquez **Enregistrer** et **Démarrer**

### 4. Appairage des appareils

1. Mettez vos appareils Ventilairsec/Enocean en mode d'appairage
2. L'addon découvre et crée automatiquement les entités
3. Consultez **Appareils et Services** dans Home Assistant

## Documentation

### Pour les utilisateurs

- [Guide d'installation complet](./INSTALL.md)
- [Appareils supportés et profilage](./docs/DEVICES.md)
- [FAQ et résolution de problèmes](./docs/FAQ.md)
- [Guide de configuration avancée](./docs/ADVANCED.md)

### Pour les développeurs

- [Architecture de l'addon](./docs/ARCHITECTURE.md)
- [Protocole Enocean - Spécifications](./docs/ENOCEAN_PROTOCOL.md)
- [Contribution - Guide du développeur](./CONTRIBUTING.md)

## Structure du projet

```
├── addons/
│   └── ventilairsec_enocean/        # Addon Home Assistant
│       ├── addon.yaml               # Configuration HA
│       ├── Dockerfile               # Image Docker
│       ├── run.sh                   # Script de démarrage
│       └── rootfs/
│           └── app/
│               ├── main.py          # Point d'entrée
│               ├── enocean_daemon.py      # Communication Enocean
│               ├── homeassistant_bridge.py # Intégration HA
│               └── device_config.py       # Profils d'appareils
│
├── ExemplePluginJeedom/             # Référence - Plugin Jeedom
│   ├── openenocean/                 # Plugin Enocean pour Jeedom
│   └── ventilairsec/                # Plugin Ventilairsec pour Jeedom
│
├── docs/                            # Documentation
├── .github/workflows/               # CI/CD (GitHub Actions)
└── README.md                        # Ce fichier
```

## Entités créées

### Capteurs (Sensors)

| Entité | Type | Description | Unité |
|--------|------|-------------|-------|
| `sensor.ventilairsec_temperature` | float | Température ambiante | °C |
| `sensor.ventilairsec_humidity` | float | Humidité relative | % |
| `sensor.ventilairsec_co2` | int | Niveau CO2 | ppm |

### Ventilateur (Fan)

| Entité | Type | Description |
|--------|------|-------------|
| `fan.ventilairsec_fan` | float | Vitesse ventilation (0-100%) |

### Commutateurs (Switch)

| Entité | Type | Description |
|--------|------|-------------|
| `switch.ventilairsec_boost` | bool | Mode boost ventilation |
| `switch.ventilairsec_power` | bool | Alimentation système |

## Exemples d'automatisations

### Augmenter ventilation si humidité trop haute

```yaml
automation:
  - alias: "Ventilation automatique sur humidité"
    trigger:
      platform: numeric_state
      entity_id: sensor.ventilairsec_humidity
      above: 65
    action:
      service: fan.set_percentage
      data:
        entity_id: fan.ventilairsec_fan
        percentage: 100
```

### Réduire ventilation la nuit

```yaml
automation:
  - alias: "Ventilation nocturne réduite"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      service: fan.set_percentage
      data:
        entity_id: fan.ventilairsec_fan
        percentage: 30
```

## Appareils supportés

### Principaux

- ✅ **Ventilairsec VMI Purevent D1079-01-00** - Thermostat intelligent
- ✅ **Capteurs Enocean 4BS** (A5-20-01) - Température/Humidité
- ✅ **Capteurs Enocean 1BS** (D5) - Contact, présence

### Voir [DEVICES.md](./docs/DEVICES.md) pour la liste complète

## Configuration avancée

### Port série personnalisé

```yaml
# Options de l'addon
serial_port: /dev/ttyUSB1       # Au lieu de /dev/ttyUSB0
serial_rate: 115200             # Vitesse (généralement 115200)
socket_port: 55006              # Port de communication interne
cycle_time: 0.3                 # Temps de cycle (en secondes)
debug_logging: false            # Activer logs détaillés
```

### Appareils personnalisés

Pour ajouter le support d'un nouvel appareil, consultez [ARCHITECTURE.md](./docs/ARCHITECTURE.md).

## Troubleshooting

### L'addon ne démarre pas

```bash
# Vérifier le port série
ls -la /dev/tty*

# Vérifier les permissions
sudo usermod -a -G dialout homeassistant
```

### Pas de découverte des appareils

1. Activez **Debug logging** dans les options de l'addon
2. Consultez les **Logs** pour identifier le problème
3. Assurez-vous que les appareils sont en mode d'appairage

### Voir [FAQ.md](./docs/FAQ.md) pour plus de solutions

## Performance et limites

- **Portée Enocean** : ~30m en direct, ~100m en champ libre
- **Débit** : Jusqu'à 125 appareils (limité par le dongle)
- **Latence** : < 1 seconde (typique)
- **Overhead CPU** : < 2% (sur Raspberry Pi 4)

## Logs et débogage

Pour activer les logs détaillés :

1. Allez à **Options** de l'addon
2. Activez **debug_logging: true**
3. Consultez les **Logs**

Exemple de sortie :

```
2024-01-15 10:23:45 - ventilairsec_enocean.daemon - INFO - Port série ouvert
2024-01-15 10:23:46 - ventilairsec_enocean.daemon - DEBUG - Paquet reçu: type=1
2024-01-15 10:23:47 - ventilairsec_enocean.bridge - INFO - Nouvel appareil: enocean_a5f12345
```

## Architecture

```
Home Assistant
    ↓
Addon Container
    ├─ enocean_daemon.py       ← Communication USB/Série
    ├─ homeassistant_bridge.py ← Intégration HA
    └─ device_config.py        ← Profils d'appareils
    ↓
Dongle Enocean USB
    ↓
Appareils Ventilairsec/Enocean
```

## Contributions

Les contributions sont les bienvenues ! 🎉

- **Issues** : Signalez les bugs
- **Pull Requests** : Proposez des améliorations
- **Documentation** : Améliorez les guides

Voir [CONTRIBUTING.md](./CONTRIBUTING.md) pour les directives.

## Licence

Ce projet est distribué sous la licence **GNU General Public License v3.0**.

Voir [LICENSE](./LICENSE) pour les détails.

## Crédits

- 🇫🇷 **Ventilairsec** - Fabricant des VMI Purevent
- 📻 **Enocean** - Protocole de communication sans fil
- 🏠 **Home Assistant** - Plateforme domotique

## Support et contact

- 📖 [Documentation](./docs/)
- 🐛 [Issues GitHub](https://github.com/fortinric88/Ventilairsec2HA/issues)
- 💬 [Discussions](https://github.com/fortinric88/Ventilairsec2HA/discussions)

---

**Dernière mise à jour** : 2024-12-29  
**Version** : 1.0.0  
**Statut** : ✅ Production stable
