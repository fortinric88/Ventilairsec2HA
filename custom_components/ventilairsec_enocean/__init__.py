"""Ventilairsec Enocean integration.

This integration connects Home Assistant to the OpenEnocean daemon
and exposes basic sensors and services to interact with VMI devices.
"""
from __future__ import annotations

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers.typing import ConfigType

from .coordinator import VentilairsecCoordinator

DOMAIN = "ventilairsec_enocean"
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data.get(CONF_HOST, "127.0.0.1")
    port = entry.data.get(CONF_PORT, 55006)

    coordinator = VentilairsecCoordinator(hass, host=host, port=port)
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await coordinator.async_start()

    # Forward platforms
    hass.config_entries.async_setup_platforms(entry, ["sensor"])

    # register services
    async def async_send_msc(call):
        payload = call.data.get("message")
        await coordinator.send_message({"cmd": "send", "message": payload})

    hass.services.async_register(DOMAIN, "send_msc", async_send_msc)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator: VentilairsecCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
    await coordinator.async_stop()
    return True
