# 🚀 GUIDE DE DÉPLOIEMENT - Post-Corrections

## ⚠️ IMPORTANT: ÉTAPES REQUISES AVANT UTILISATION

Avant de redéployer le module dans Home Assistant, suivez ces étapes:

---

## 1️⃣ PRÉPARER HOME ASSISTANT

### Pré-requis
- [ ] Home Assistant 2023.10.0 ou plus récent
- [ ] Broker MQTT installé et fonctionnel
- [ ] Dongle Enocean USB connecté

### Vérifications

```bash
# 1. Vérifier la version de Home Assistant
# Aller à: Settings → System → About

# 2. Vérifier MQTT
# Aller à: Settings → Devices & Services → MQTT
# L'addon "Mosquitto broker" doit être en vert "Connected"

# 3. Vérifier le dongle Enocean
# Terminal SSH:
ls -la /dev/ttyUSB*
ls -la /dev/ttyACM*
# Vous devriez voir au moins un périphérique
```

---

## 2️⃣ AJOUTER LE REPOSITORY (SI NÉCESSAIRE)

1. Allez à **Settings → Add-ons → Add-on store** (coin en bas à droite)
2. Cliquez sur les trois points → **Repositories**
3. Ajoutez cette URL:
   ```
   https://github.com/fortinric88/Ventilairsec2HA
   ```
4. Cliquez "Create"

---

## 3️⃣ INSTALLER L'ADDON

1. **Settings → Add-ons → Add-on store**
2. Recherchez **"Ventilairsec Enocean"**
3. Cliquez sur l'addon
4. Cliquez **"Install"**

*Attendez la fin du téléchargement et de la compilation de l'image Docker*

---

## 4️⃣ CONFIGURER L'ADDON

Une fois l'installation terminée, cliquez sur l'addon pour accéder à la configuration.

### Configuration Obligatoire

#### Serial Port
- **Sélectionnez le port USB** où votre dongle Enocean est connecté
- Généralement: `/dev/ttyUSB0` ou `/dev/ttyACM0`
- Pour trouver le bon port: Terminal SSH → `ls -la /dev/tty*`

#### Serial Rate
- **Laisser par défaut: 57600** (Baud)
- Ne changer que si spécifié dans la doc de votre dongle

#### MQTT Broker
- **Par défaut: localhost**
- Si vous utilisez une adresse IP: `192.168.1.100` (par exemple)

#### MQTT Port
- **Par défaut: 1883** (non chiffré)
- **Recommandé: 8883** (avec TLS chiffré) - si votre broker le supporte

#### MQTT User
- Votre nom d'utilisateur MQTT
- Peut être vide si pas d'authentification (non recommandé)

#### MQTT Password
- Votre mot de passe MQTT
- Sera chiffré par Home Assistant
- Peut être vide si pas d'authentification (non recommandé)

#### MQTT Use TLS ⭐
- **Désactivé par défaut** (false)
- **À ACTIVER** si vous utilisez le port 8883 avec TLS

#### Debug Logging
- **Désactivé par défaut** (false)
- Activer seulement pour diagnostiquer des problèmes

### Configuration Recommandée (Sécurisée)

```yaml
serial_port: /dev/ttyUSB0
serial_rate: 57600
mqtt_broker: localhost      # ou 192.168.1.100
mqtt_port: 8883             # Port TLS
mqtt_user: ventilairsec
mqtt_password: <password_fort>
mqtt_use_tls: true          # ✅ ACTIVÉ
debug_logging: false
```

---

## 5️⃣ DÉMARRER L'ADDON

1. Cliquez sur l'addon Ventilairsec Enocean
2. Cliquez **"Start"** (bouton bleu)
3. Attendez quelques secondes

### Vérifier le Démarrage

1. **Allez dans les Logs** (onglet "Logs" en bas de l'addon)
2. Vous devriez voir:
   ```
   Starting Ventilairsec Enocean addon...
   Configuration loaded:
     Serial port: /dev/ttyUSB0
     Serial rate: 57600 baud
     MQTT broker: localhost:1883
     Debug mode: false
   Configuration file created at /etc/ventilairsec/enoceanmqtt.conf
   Checking for serial port: /dev/ttyUSB0
   Serial port detected: /dev/ttyUSB0
   Starting Enocean daemon...
   ```

### En Cas d'Erreur

Si vous voyez une erreur comme:
```
Serial port /dev/ttyUSB0 not found after 30s timeout
Please verify your USB device is connected
```

**Solutions**:
1. Vérifiez que le dongle USB est bien connecté
2. Vérifiez le bon port avec: `ls -la /dev/tty*`
3. Changez la configuration avec le bon port
4. Relancez l'addon

---

## 6️⃣ CONFIGURER L'INTÉGRATION MQTT

Maintenant que l'addon s'exécute, configurez l'intégration MQTT dans Home Assistant.

### Configuration MQTT (Home Assistant)

1. **Settings → Devices & Services → MQTT**
2. Cliquez sur le broker Mosquitto
3. Vérifiez que les paramètres correspondent à votre config d'addon

### Ajout Automatique d'Appareils

Si tout fonctionne, Home Assistant devrait découvrir automatiquement:
- Les appareils Enocean
- Les capteurs de température/humidité
- Les contrôles de vitesse du ventilateur

Allez à **Settings → Devices & Services → Discovered** pour voir les nouveaux appareils.

---

## 7️⃣ VÉRIFIER LA CONNEXION

### Test de Connectivité MQTT

```bash
# SSH Terminal
mosquitto_sub -u ventilairsec -P <password> -h localhost -p 8883 -t "homeassistant/climate/+/config"

# Vous devriez voir des messages JSON des appareils découverts
```

### Monitorer les Données

1. **Allez à: Developer tools → States**
2. Cherchez `climate.ventilairsec_*`
3. Vous devriez voir l'état et les attributs du ventilateur

---

## 8️⃣ PROBLÈMES COURANTS ET SOLUTIONS

| Problème | Cause Probable | Solution |
|----------|-----------------|----------|
| Port série pas trouvé | Dongle non connecté | Vérifier connexion USB |
| MQTT non connecté | Broker arrêté | Redémarrer Mosquitto |
| Pas d'appareils découverts | Pas de signal Enocean | Vérifier proximité appareils |
| Erreur d'authentification MQTT | Identifiants incorrects | Vérifier user/password |
| TLS erreur | Port/TLS mismatch | Vérifier port (1883 vs 8883) |

---

## 9️⃣ SÉCURITÉ - VÉRIFICATIONS FINALES

Une fois l'addon en cours d'exécution:

- [ ] Les logs ne montrent pas d'erreurs de sécurité
- [ ] MQTT est connecté avec authentification
- [ ] Le fichier config a les permissions correctes (0600)
- [ ] Aucun mot de passe visible dans les logs
- [ ] TLS est activé si supporté (port 8883)

### Vérifier les Permissions (SSH)

```bash
# Terminal SSH
ls -l /etc/ventilairsec/enoceanmqtt.conf

# Vous devriez voir: -rw------- (permissions 0600)
# Si vous voyez: -rw-r--r-- (permissions 0644) → PROBLÈME DE SÉCURITÉ !
```

---

## 🔟 AUTO-DÉMARRAGE

Pour que l'addon démarre automatiquement avec Home Assistant:

1. Cliquez sur l'addon Ventilairsec Enocean
2. **Cochez "Start on boot"** (en haut)
3. **Cochez "Watchdog"** (pour redémarrage automatique en cas de crash)
4. Cliquez **"Save"**

---

## 📝 NOTES IMPORTANTES

### ✅ Après Ces Corrections:
- Le code ne contient plus d'erreurs syntaxe Python
- La validation des paramètres évite les crashes
- Les permissions de fichiers sécurisent les mots de passe
- Le timeout du port série gère les USB lents
- TLS est maintenant supporté pour la sécurité

### ⚠️ À Savoir:
- Les mots de passe MQTT ne doivent JAMAIS être commit dans Git
- Utilisez les secrets de Home Assistant pour stocker les identifiants
- Ne partagez jamais le contenu de `/etc/ventilairsec/enoceanmqtt.conf`
- Maintenez Home Assistant et l'addon à jour

### 🔄 Mise à Jour Future:
Quand une nouvelle version est disponible:
1. L'addon vous notifiera dans Home Assistant
2. Cliquez "Update"
3. L'addon redémarre automatiquement
4. Vérifiez les logs après la mise à jour

---

## 📞 SUPPORT

Si vous rencontrez un problème:

1. **Consultez les logs** de l'addon (onglet "Logs")
2. **Activez le debug** (Debug logging: true) et relancez l'addon
3. **Ouvrez une issue** sur GitHub: https://github.com/fortinric88/Ventilairsec2HA/issues
4. **Partagez les logs** (sans les mots de passe !)

---

## ✅ CHECKLIST FINALE

- [ ] Home Assistant 2023.10.0+
- [ ] MQTT broker fonctionnel
- [ ] Dongle Enocean connecté
- [ ] Repository ajouté
- [ ] Addon installé
- [ ] Configuration complétée
- [ ] Addon démarré sans erreur
- [ ] Appareils découverts
- [ ] Connexion MQTT établie
- [ ] Auto-démarrage activé

---

**Vous êtes prêt! 🎉**

L'addon Ventilairsec Enocean devrait maintenant fonctionner correctement et sécurisément.
