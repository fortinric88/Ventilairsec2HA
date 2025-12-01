from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class VentilairsecCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, host: str = "127.0.0.1", port: int = 55006) -> None:
        super().__init__(hass, _LOGGER, name="ventilairsec_enocean", update_interval=None)
        self.host = host
        self.port = port
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self.data: dict[str, Any] = {}
        self._task: asyncio.Task | None = None

    async def async_start(self) -> None:
        self._task = asyncio.create_task(self._connect_loop())

    async def async_stop(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()

    async def _connect_loop(self) -> None:
        while True:
            try:
                _LOGGER.debug("Connecting to openenoceand %s:%s", self.host, self.port)
                self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
                _LOGGER.info("Connected to openenoceand at %s:%s", self.host, self.port)
                await self._read_loop()
            except Exception as exc:  # reconnect on error
                _LOGGER.warning("Connection error: %s, reconnecting in 5s", exc)
                await asyncio.sleep(5)

    async def _read_loop(self) -> None:
        assert self._reader is not None
        while True:
            line = await self._reader.readline()
            if not line:
                _LOGGER.info("openenoceand connection closed by peer")
                break
            try:
                message = line.decode("utf-8").strip()
                if not message:
                    continue
                obj = json.loads(message)
                self.data.update(obj)
                self.async_set_updated_data(self.data)
            except Exception as e:
                _LOGGER.debug("Failed to parse message: %s", e)

    async def send_message(self, message: dict) -> None:
        if not self._writer:
            raise ConnectionError("Not connected to openenoceand")
        data = json.dumps(message) + "\n"
        self._writer.write(data.encode("utf-8"))
        await self._writer.drain()
