# Politique de Sécurité - Ventilairsec Enocean Addon

## Sécurité des Données

### Authentification MQTT

**IMPORTANT**: Pour des raisons de sécurité, nous recommandons fortement:

1. **Utiliser un nom d'utilisateur et mot de passe MQTT** - Ne jamais laisser le broker MQTT accessible sans authentification
2. **Activer TLS/SSL** - Changer le port à `8883` et activer l'option `mqtt_use_tls`
3. **Utiliser des mots de passe forts** - Minimum 16 caractères avec majuscules, minuscules, chiffres et symboles

### Stockage des Identifiants

Les identifiants MQTT sont stockés de manière sécurisée:
- Les mots de passe sont chiffrés par Home Assistant
- Le fichier de configuration (`/etc/ventilairsec/enoceanmqtt.conf`) a des permissions restrictives (`0600`)
- Seul l'utilisateur root peut lire le fichier de configuration

## Vulnérabilités Connues et Fixes

### ✅ Corrigé - Erreur de Syntaxe Python (CRITIQUE)
**Problème**: Utilisation de `bashio::config()` au lieu de `bashio.config()` empêchait le code de s'exécuter
**Correction**: Mise à jour de la syntaxe Python correcte
**Statut**: RÉSOLU

### ✅ Corrigé - Permissions de Fichiers de Configuration
**Problème**: Fichier config accessible en lecture à tous les utilisateurs
**Correction**: Permissions défini à `0600` (rw-------)
**Statut**: RÉSOLU

### ✅ Corrigé - Validation des Paramètres MQTT
**Problème**: Pas de validation des ports et paramètres de configuration
**Correction**: Ajout de `validate_config()` avec vérifications strictes
**Statut**: RÉSOLU

### ✅ Amélioré - Gestion du Port Série
**Problème**: Le script ne vérifiait pas la présence du port avec timeout approprié
**Correction**: Ajout d'une boucle d'attente avec timeout de 30s
**Statut**: RÉSOLU

### ✅ Amélioré - Version de l'Image Docker
**Problème**: Utilisation de `:latest` pouvant causer des incompatibilités
**Correction**: Pinning à une version spécifique (`2024.01`)
**Statut**: RÉSOLU

## Recommandations Supplémentaires

### Pour les Administrateurs Home Assistant

1. **Mise à jour Régulière**
   - Gardez Home Assistant à jour
   - Activez les mises à jour automatiques des addons

2. **Configuration Sécurisée du MQTT**
   ```yaml
   # Configuration recommandée dans Home Assistant
   mqtt:
     broker: localhost  # Ou adresse IP locale sécurisée
     port: 8883         # Port TLS
     username: !secret mqtt_user
     password: !secret mqtt_password
     tls_version: tlsv1_2
   ```

3. **Contrôle d'Accès**
   - Limitez l'accès au MQTT aux seuls devices autorisés
   - Utilisez un firewall pour restreindre les connexions entrantes

### Pour les Développeurs

1. **Code Review Sécurité**
   - Toute contribution passe par une revue de sécurité
   - Les dépendances Python doivent être validées

2. **Dépendances**
   - Les packages Python utilisés sont maintenus et sécurisés:
     - `pyserial` - Communication série
     - `paho-mqtt` - Client MQTT
     - `requests` - Requêtes HTTP
     - `cryptography` - Opérations cryptographiques
     - `pyyaml` - Parsing YAML
     - `tinydb` - Base de données légère

3. **Rapports de Sécurité**
   - Pour signaler une vulnérabilité: Ouvrir une issue privée sur GitHub
   - Ne pas publier les vulnérabilités avant correction

## Checklist de Sécurité pour l'Utilisateur

Avant de déployer l'addon:

- [ ] Home Assistant est à jour (2023.10.0 ou plus récent)
- [ ] MQTT broker utilise un mot de passe fort
- [ ] L'option `mqtt_use_tls` est activée
- [ ] Le port MQTT est configuré correctement (1883 ou 8883)
- [ ] Les identifiants MQTT sont stockés dans les secrets de Home Assistant
- [ ] Le dongle Enocean est connecté et reconnu (`/dev/ttyUSB0` ou similaire)
- [ ] Les logs ne montrent pas d'erreurs de connexion MQTT
- [ ] Firewall: le port MQTT n'est accessible que depuis la machine Home Assistant

## Contact Sécurité

Pour toute question de sécurité: **fortinric88 <https://github.com/fortinric88>**
