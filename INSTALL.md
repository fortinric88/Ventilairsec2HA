# Guide d'Installation du Dépôt Ventilairsec Home Assistant

Ce guide explique comment installer le dépôt d'addons Ventilairsec dans Home Assistant.

## Méthode 1 : Ajouter le dépôt via l'interface

### Étape 1 : Accéder à la gestion des addons

1. Ouvrez Home Assistant
2. Allez à **Paramètres** (en bas à gauche)
3. Cliquez sur **Modules complémentaires**
4. Cliquez sur le bouton **Créer et gérer** (en haut à droite)

### Étape 2 : Ajouter le dépôt

1. Cliquez sur les **trois points** (⋮) en haut à droite
2. Sélectionnez **Dépôts**
3. Dans le champ **Ajouter**, entrez l'URL du dépôt:
   ```
   https://github.com/fortinric88/Ventilairsec2HA
   ```
4. Cliquez sur **Créer**

### Étape 3 : Installer l'addon

1. Retournez à **Modules complémentaires**
2. Cherchez "Ventilairsec Enocean"
3. Cliquez sur l'addon
4. Cliquez sur **Installer**

## Méthode 2 : Installation manuelle

### Prérequis

- Accès SSH à votre système Home Assistant
- Le dossier `addons` doit exister dans `/config/`

### Étapes

```bash
# 1. Se connecter en SSH
ssh <user>@<home-assistant-ip>

# 2. Accéder au répertoire addons
cd /config/addons

# 3. Cloner le dépôt
git clone https://github.com/fortinric88/Ventilairsec2HA
cd Ventilairsec2HA

# 4. Retourner à Home Assistant
cd /config

# 5. Redémarrer Home Assistant
# Via l'interface : Paramètres > Système > Redémarrer
```

Après le redémarrage :
1. Allez à **Modules complémentaires**
2. Vous devriez voir le nouvel addon
3. Installez-le

## Configuration de l'addon

Une fois installé :

1. Cliquez sur l'addon **Ventilairsec Enocean**
2. Allez à **Options**
3. Configurez :
   - **Port série** : Où votre dongle Enocean est connecté
   - **Autres paramètres** selon vos besoins
4. Cliquez sur **Enregistrer**
5. Allez à **Info** et cliquez sur **Démarrer**

## Vérification du fonctionnement

### Vérifier que le dongle Enocean est détecté

```bash
# Via SSH
ls -la /dev/tty*

# Cherchez : /dev/ttyUSB0, /dev/ttyUSB1, /dev/ttyACM0, etc.
```

### Consulter les logs

1. Dans l'addon, cliquez sur **Logs**
2. Vous devriez voir les messages de démarrage

### Logs typiques de fonctionnement

```
=== Démarrage de l'addon Ventilairsec Enocean ===
Configuration chargée:
  Port série: /dev/ttyUSB0
  Vitesse: 115200 baud
  Port socket: 55006
  Cycle: 0.3 s
  Debug: False

Port série détecté: /dev/ttyUSB0
Lancement du daemon Enocean...
Daemon Enocean démarré
Pont Home Assistant lancé
```

## Résolution des problèmes

### L'addon refuse de démarrer

**Cause possible** : Port série invalide

**Solution** :
1. Vérifiez le port avec `ls /dev/tty*`
2. Mettez à jour les **Options** avec le bon port
3. Redémarrez l'addon

### L'addon démarre mais pas de découverte

**Cause possible** : Aucun appareil Enocean à proximité ou pas en mode d'appairage

**Solution** :
1. Activez le **mode d'appairage** sur vos appareils Ventilairsec
2. Attendez 60 secondes
3. Vérifiez les **Appareils et Services** dans Home Assistant

### Erreur de permissions

**Cause possible** : L'addon n'a pas les permissions de lecture/écriture sur le port série

**Solution** :
1. Via SSH, ajoutez les permissions :
   ```bash
   sudo usermod -a -G dialout homeassistant
   ```
2. Redémarrez Home Assistant

## Mise à jour

L'addon se met à jour automatiquement si vous avez activé les mises à jour automatiques.

Pour mettre à jour manuellement :

1. Allez à **Modules complémentaires**
2. Cherchez "Ventilairsec Enocean"
3. Si une mise à jour est disponible, cliquez sur **Mettre à jour**

## Support

En cas de problème :

1. Consultez les **Logs** dans l'addon
2. Essayez d'activer **Debug logging** dans les options
3. Créez une issue : https://github.com/fortinric88/Ventilairsec2HA/issues

## Documentation supplémentaire

- [Configuration de l'addon](./addons/ventilairsec_enocean/README.md)
- [Appareils supportés](./docs/DEVICES.md)
- [FAQ et dépannage](./docs/FAQ.md)
