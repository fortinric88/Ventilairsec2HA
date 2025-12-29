#!/usr/bin/env bash
set -e

# Coleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Démarrage de l'addon Ventilairsec Enocean ===${NC}"

# Créer les répertoires nécessaires
mkdir -p /var/log/ventilairsec
mkdir -p /etc/ventilairsec
mkdir -p /var/lib/ventilairsec

# Obtenir les paramètres de configuration
SERIAL_PORT=$(bashio::config 'serial_port')
SERIAL_RATE=$(bashio::config 'serial_rate')
SOCKET_PORT=$(bashio::config 'socket_port')
CYCLE_TIME=$(bashio::config 'cycle_time')
DEBUG_LOGGING=$(bashio::config 'debug_logging')

echo -e "${GREEN}Configuration chargée:${NC}"
echo "  Port série: $SERIAL_PORT"
echo "  Vitesse: $SERIAL_RATE baud"
echo "  Port socket: $SOCKET_PORT"
echo "  Cycle: $CYCLE_TIME s"
echo "  Debug: $DEBUG_LOGGING"

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

echo -e "${GREEN}Configuration sauvegardée${NC}"

# Vérifier la disponibilité du port série
if [ ! -c "$SERIAL_PORT" ]; then
    echo -e "${RED}ERREUR: Port série $SERIAL_PORT non disponible${NC}"
    echo -e "${YELLOW}Attendez et réessayez...${NC}"
    exit 1
fi

echo -e "${GREEN}Port série détecté: $SERIAL_PORT${NC}"

# Démarrer le daemon Enocean
echo -e "${GREEN}Lancement du daemon Enocean...${NC}"
cd /app
exec python3 -u main.py 2>&1
