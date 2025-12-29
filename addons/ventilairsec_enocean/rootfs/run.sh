#!/usr/bin/env bash
set -e

# Coleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

source /usr/lib/bashio/bashio.sh

echo -e "${GREEN}=== Initialisation de l'addon Ventilairsec Enocean ===${NC}"

# Obtenir les paramètres de configuration
SERIAL_PORT=$(bashio::config 'serial_port')
SERIAL_RATE=$(bashio::config 'serial_rate')
SOCKET_PORT=$(bashio::config 'socket_port')
CYCLE_TIME=$(bashio::config 'cycle_time')
DEBUG_LOGGING=$(bashio::config 'debug_logging')

bashio::log.info "Configuration chargée:"
bashio::log.info "  Port série: $SERIAL_PORT"
bashio::log.info "  Vitesse: $SERIAL_RATE baud"
bashio::log.info "  Port socket: $SOCKET_PORT"
bashio::log.info "  Cycle: $CYCLE_TIME s"
bashio::log.info "  Debug: $DEBUG_LOGGING"

# Créer les répertoires nécessaires
mkdir -p /var/log/ventilairsec
mkdir -p /etc/ventilairsec
mkdir -p /var/lib/ventilairsec

# Créer le fichier de configuration Python
cat > /etc/ventilairsec/config.ini << EOF
[enocean]
serial_port = $SERIAL_PORT
serial_rate = $SERIAL_RATE
socket_port = $SOCKET_PORT
cycle_time = $CYCLE_TIME
debug_logging = $DEBUG_LOGGING

[homeassistant]
host = supervisor
port = 8123
token = \${SUPERVISOR_TOKEN}
EOF

bashio::log.info "Configuration sauvegardée dans /etc/ventilairsec/config.ini"

# Vérifier la disponibilité du port série
if [ ! -c "$SERIAL_PORT" ]; then
    bashio::log.error "Port série $SERIAL_PORT non disponible"
    bashio::log.warning "Attendez quelques secondes et réessayez..."
    # Ne pas sortir ici, le daemon tentera de se reconnecter
fi

bashio::log.info "Port série détecté: $SERIAL_PORT"
