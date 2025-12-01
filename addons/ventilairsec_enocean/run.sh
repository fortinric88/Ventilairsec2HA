#!/bin/bash
set -e

# Simple run script for the openenoceand daemon copied into the image.
DEVICE="${DEVICE:-auto}"
PORT="${PORT:-55006}"
APIKEY="${APIKEY:-}" 

if [ ! -d /openenoceand ]; then
  echo "openenoceand not found in image; exiting"
  exit 1
fi

cd /openenoceand
exec python3 openenoceand.py --device "${DEVICE}" --socketport "${PORT}" --apikey "${APIKEY}"
