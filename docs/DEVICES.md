# Appareils Supportés

Liste des appareils Ventilairsec et Enocean supportés par l'addon.

## VMI Purevent Ventilairsec

### D1079-01-00 (Thermostat Intelligent)

**Caractéristiques** :
- Profil Enocean: 4BS (A5-20-01)
- Capteurs: Température, Humidité
- Commandes: Contrôle ventilation (vitesse)
- Portée: ~30m en direct, ~100m en champ libre

**Entités Home Assistant créées** :

| Entité | Type | Unité | Description |
|--------|------|-------|-------------|
| `sensor.ventilairsec_temperature` | Capteur | °C | Température ambiante |
| `sensor.ventilairsec_humidity` | Capteur | % | Humidité relative |
| `fan.ventilairsec_fan` | Ventilateur | 0-100 | Vitesse ventilation |
| `switch.ventilairsec_power` | Commutateur | - | Alimentation |

**Exemple de configuration** :

```yaml
# Émettre des commandes à la VMI
service: fan.set_percentage
data:
  entity_id: fan.ventilairsec_fan
  percentage: 75  # 0-100
```

---

## Capteurs Enocean génériques

### Capteurs 4BS (A5-20-01) - Température/Humidité

**Caractéristiques** :
- Profil: 4-byte Communication (4BS)
- Capteurs: Température (−40°C à +62°C), Humidité (0-100%)
- Alimentation: Batteries ou secteur
- Portée: ~30m

**Exemples** :
- Eltako FTF-hE
- Gledopto
- Autres capteurs A5-20-01

**Entités créées** :
- `sensor.<device>_temperature`
- `sensor.<device>_humidity`

### Capteurs 1BS (D5) - Contact et Boutons

**Caractéristiques** :
- Profil: 1-byte Communication (1BS)
- Types: Capteur de contact, boutons, détecteurs
- Alimentation: Batteries
- Portée: ~30m

**Types supportés** :
- D5-00-01 : Capteur de contact (porte, fenêtre)
- D5-00-02 : Capteur de mouvement/présence

**Entités créées** :
- `binary_sensor.<device>_contact`
- `binary_sensor.<device>_presence`

### Communication Variable (D2)

**Caractéristiques** :
- Profil: Variable Length Data (VLD)
- Données: Variables selon l'appareil
- Utilité: Capteurs spécialisés, modules intelligents

**Support** : Décodage générique, détails dans les logs

---

## Protocole Enocean - Profils Supportés

| Code | Nom | Données | Support |
|------|-----|---------|---------|
| 0xA5 | 4-byte (4BS) | 4 octets | ✅ Complet |
| 0xD5 | 1-byte (1BS) | 1 octet | ✅ Complet |
| 0xD2 | Variable (VLD) | Variable | ⚠️ Basique |
| 0xD1 | Ventilateur smart | 3+ octets | ✅ Complet |

---

## Ajout de nouveaux appareils

### Pour un appareil spécifique

Si vous avez un appareil non reconnu automatiquement :

1. **Relevez l'ID Enocean** (consulter les logs en mode debug)
2. **Créez un profil** dans `device_config.py`
3. **Testez et soumettez** une pull request

### Exemple de profil personnalisé

```python
# Dans device_config.py
'D1079-02-00': {
    'name': 'VMI Purevent D1079-02-00',
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
        'co2': {
            'type': 'sensor',
            'name': 'CO2',
            'unit': 'ppm'
        }
    }
}
```

---

## Appareils testés et validés

### Certifiés

- ✅ Ventilairsec VMI Purevent D1079-01-00
- ✅ Capteurs Eltako FTF-hE

### En cours de test

- 🔄 Autres modèles Ventilairsec
- 🔄 Capteurs Gledopto

### En demande

Créez une issue pour demander le support d'un appareil spécifique :
https://github.com/fortinric88/Ventilairsec2HA/issues

---

## Configuration par appareil

### Ventilairsec VMI Purevent

**Activation du mode Enocean** :

Consultez le manuel d'installation fourni avec votre VMI. Généralement :
1. Accédez au menu de configuration
2. Activez le protocole Enocean
3. Mettez en mode d'appairage
4. Attendez la découverte par l'addon

### Capteurs Enocean tiers

**Appairage typique** :

1. Mettez le capteur en mode d'apprentissage (bouton long)
2. Lancez la découverte dans l'addon
3. Le capteur apparaît après quelques secondes

---

## Limitations connues

- ⚠️ Les données bipolaires (switchable) ne sont pas encore supportées
- ⚠️ Certains profils avancés peuvent nécessiter des développements
- ⚠️ La portée Enocean est limitée (~30m direct)

---

## Support et contributions

Pour ajouter le support d'un nouvel appareil :

1. Créez une issue avec l'ID Enocean
2. Fournissez les spécifications du protocole
3. Proposez une pull request avec le profil

Documentation Enocean officielle :
https://www.enocean.com/en/enocean-modules/
