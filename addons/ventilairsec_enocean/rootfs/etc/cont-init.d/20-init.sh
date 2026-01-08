#!/bin/sh
# Initialize required directories and files

set -e

# Create required directories
mkdir -p /var/log/ventilairsec
mkdir -p /var/lib/ventilairsec
mkdir -p /etc/ventilairsec

# Create example config if not exists
if [ ! -f /etc/ventilairsec/enoceanmqtt.conf ]; then
    cp /etc/enoceanmqtt.conf.sample /etc/ventilairsec/enoceanmqtt.conf
fi

echo "Directories and configuration initialized"

