#!/usr/bin/env bash

set -e

# Installer bashio
if [ ! -f /usr/lib/bashio/bashio.sh ]; then
    echo "Installation de bashio..."
    mkdir -p /tmp
    cd /tmp
    wget -q https://github.com/hassio-addons/bashio/archive/master.tar.gz
    tar xzf master.tar.gz
    mkdir -p /usr/lib/bashio
    cp bashio-master/lib/* /usr/lib/bashio/
    rm -rf /tmp/bashio* /tmp/master.tar.gz
fi

echo "Installation complète"
