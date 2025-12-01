from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT

from . import DOMAIN


class VentilairsecConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Ventilairsec Enocean", data=user_input)

        schema = vol.Schema({vol.Required(CONF_HOST, default="127.0.0.1"): str, vol.Required(CONF_PORT, default=55006): int})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
