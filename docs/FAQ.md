# FAQ - Questions Fréquentes

## Installation et configuration

### Q: Comment identifier mon port série Enocean?

**R:** 

```bash
# Via SSH dans votre système
ls -la /dev/tty*

# Vous devriez voir :
# /dev/ttyUSB0 ou /dev/ttyUSB1 (dongle USB)
# /dev/ttyACM0 ou /dev/ttyACM1 (port série émulé)

# Pour confirmer :
dmesg | tail -20
# Cherchez la ligne d'énumération USB avec la vitesse 115200
```

### Q: L'addon refuse de démarrer "Port non disponible"

**R:** Plusieurs solutions :

1. **Vérifiez la connexion** :
   - Débranchez/rebranchez le dongle USB
   - Attendez 5 secondes
   - Redémarrez l'addon

2. **Changez de port USB** :
   - Connectez le dongle à un autre port
   - Mettez à jour `serial_port` dans les options

3. **Permissions** (Raspberry Pi, NAS) :
   ```bash
   sudo usermod -a -G dialout homeassistant
   # Redémarrez Home Assistant
   ```

### Q: Comment configurer le port `/dev/ttyUSB1` au lieu de `/dev/ttyUSB0`?

**R:**

1. Allez à l'addon **Ventilairsec Enocean**
2. Onglet **Configuration**
3. Changez `serial_port` de `/dev/ttyUSB0` à `/dev/ttyUSB1`
4. Cliquez **Enregistrer**
5. Redémarrez l'addon

## Appareils et découverte

### Q: Aucun appareil n'est découvert

**R:** Vérifiez ces points dans cet ordre :

1. **Le dongle fonctionne** :
   - Vérifiez les logs (Onglet Logs)
   - Cherchez "Port série détecté"

2. **L'appareil est en mode apprentissage** :
   - Pour Ventilairsec : Menu configuration → Enocean → Apprentissage
   - Pour capteurs : Bouton long (généralement 10 secondes)

3. **Distance et portée** :
   - Approchez le dongle de l'appareil (< 10m)
   - Évitez obstacles métalliques
   - Attendez 60 secondes

4. **Activez debug logging** :
   - Configuration → `debug_logging: true`
   - Redémarrez
   - Consultez les logs détaillés

### Q: Je vois l'appareil mais pas les entités

**R:**

1. Attendez 10-20 secondes après la découverte
2. Rechargez la page **Appareils et Services**
3. Cherchez un nouvel appareil `enocean_XXXXXXXX`
4. Les entités doivent être créées automatiquement

### Q: Comment renommer les appareils?

**R:**

1. Allez à **Appareils et Services**
2. Trouvez l'appareil Enocean
3. Cliquez sur l'appareil
4. Modifiez le **Nom** en haut

Les entités sont associées automatiquement.

## Performance et stabilité

### Q: L'communication est lente ou saccadée

**R:** Essayez :

1. **Réduisez le cycle de traitement** :
   - Configuration → `cycle_time: 0.2`
   - Redémarrez

2. **Optimisez la position du dongle** :
   - Placez-le au centre de votre maison
   - Surélevez-le (sur une étagère)
   - Éloignez des sources d'interférence (WiFi, fours)

3. **Réduisez le nombre d'appareils** :
   - Le dongle supporte ~125 appareils
   - Désactivez les appareils inutilisés

### Q: L'addon consomme beaucoup de CPU

**R:** C'est anormal. Vérifiez :

1. **Logs d'erreurs** :
   - Activez debug et cherchez les erreurs
   - Rapportez dans une issue GitHub

2. **Nombre d'appareils** :
   - Trop d'appareils peuvent surcharger
   - Commencez par 2-3 appareils

3. **Configuration cycle_time** :
   - Augmentez-la si processeur faible (RPi Zero)
   - Défaut 0.3s est bon pour RPi 4

## Automatisations et contrôle

### Q: Comment créer une automatisation avec le ventilateur?

**R:** Exemple :

```yaml
automation:
  - alias: "Augmenter ventilation si humidité > 65%"
    trigger:
      platform: numeric_state
      entity_id: sensor.ventilairsec_XXXXXXXX_humidity
      above: 65
    action:
      - service: fan.set_percentage
        data:
          entity_id: fan.ventilairsec_XXXXXXXX_fan
          percentage: 100
      - delay: "00:30:00"  # 30 minutes
      - service: fan.set_percentage
        data:
          entity_id: fan.ventilairsec_XXXXXXXX_fan
          percentage: 50
```

### Q: Comment créer un script pour éteindre le ventilateur la nuit?

**R:**

```yaml
script:
  ventilation_nocturne:
    sequence:
      - service: fan.set_percentage
        data:
          entity_id: fan.ventilairsec_XXXXXXXX_fan
          percentage: 20
```

Puis créez une automatisation :

```yaml
automation:
  - alias: "Ventilation réduite la nuit"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      - service: script.ventilation_nocturne
```

## Dépannage avancé

### Q: Comment voir les paquets Enocean bruts?

**R:**

1. Activez `debug_logging: true`
2. Consultez les logs
3. Vous verrez les données hexadécimales :
   ```
   Paquet radio: RORG=A5, ID=a5f12345, Status=80
   ```

### Q: L'addon crash aléatoirement

**R:** Collectez les logs :

1. Activez debug logging
2. Attendez le crash
3. Copiez les 50 dernières lignes de log
4. Créez une issue GitHub avec les logs

### Q: Puis-je avoir 2 dépôts Enocean?

**R:** Oui, mais:

- Chacun doit avoir son propre dongle USB
- Chacun doit être sur un port série différent
- Créez 2 instances de l'addon

```bash
# Instance 1
serial_port: /dev/ttyUSB0

# Instance 2
serial_port: /dev/ttyUSB1
```

## Ventilairsec spécifique

### Q: Comment activer le protocole Enocean sur ma VMI Purevent?

**R:** Consultez le manuel de votre VMI :

1. Menu configuration (généralement avec contrôleur mural)
2. Cherchez "Protocole" ou "Enocean"
3. Activez Enocean
4. Entrez en mode apprentissage (learning mode)
5. L'addon découvrira automatiquement

### Q: Comment savoir si ma VMI supporte Enocean?

**R:** Vérifiez :

1. **Manuel de l'utilisateur** - Cherchez "Enocean" ou "protocol"
2. **Plaque signalétique** - Modèles supportés : D1079-01-00, D1079-02-00
3. **Support Ventilairsec** - info@ventilairsec.com

### Q: Puis-je contrôler la VMI à distance?

**R:** Oui ! Une fois intégrée :

```yaml
service: fan.set_percentage
data:
  entity_id: fan.ventilairsec_XXXXXXXX_fan
  percentage: 80
```

Cela fonctionne aussi de l'extérieur si Home Assistant est accessible.

## Mise à jour et maintenance

### Q: L'addon se met-il à jour automatiquement?

**R:** Oui, si vous avez coché la case dans Home Assistant :

**Paramètres** → **Système** → **Mises à jour** → Activer pour l'addon

Pour mettre à jour manuellement :
1. Allez à l'addon
2. Si une mise à jour est disponible, cliquez **Mettre à jour**

### Q: Que se passe-t-il si je mets à jour Home Assistant?

**R:** L'addon reste compatible. Generalement :

1. Home Assistant se met à jour
2. Redémarre
3. L'addon se relance automatiquement
4. Tout fonctionne comme avant

### Q: Comment désinstaller l'addon?

**R:**

1. Allez à l'addon **Ventilairsec Enocean**
2. Cliquez les trois points ⋮
3. **Supprimer**

Les entités restent dans Home Assistant (créez une automatisation pour les supprimer si nécessaire).

## Limite et compatibilité

### Q: Quels ports USB sont supportés?

**R:** Tous les ports USB standard :

- `/dev/ttyUSB0`, `/dev/ttyUSB1` - Convertisseurs USB→série
- `/dev/ttyACM0`, `/dev/ttyACM1` - Ports série natifs
- `/dev/ttyAMA0` - Raspberry Pi (UART GPIO)

### Q: Quels appareils Enocean fonctionne?

**R:** Voir [DEVICES.md](../docs/DEVICES.md)

Supportés :
- ✅ Ventilairsec VMI Purevent
- ✅ Capteurs Eltako FTF
- ✅ Capteurs génériques 4BS et 1BS

### Q: Quelle est la consommation électrique?

**R:** Très faible :

- Addon : ~1W (CPU usage)
- Dongle USB : ~0.5W
- Total : ~1.5W

Peut tourner 24/7 sans problème.

## Besoin d'aide?

- 📖 [Documentation complète](../README.md)
- 🐛 [Issues GitHub](https://github.com/fortinric88/Ventilairsec2HA/issues)
- 💬 [Discussions](https://github.com/fortinric88/Ventilairsec2HA/discussions)

---

**Dernière mise à jour** : 2024-12-29
