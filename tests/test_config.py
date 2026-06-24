from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from discord_auto_role.config import ConfigError, load_settings


class LoadSettingsTestCase(unittest.TestCase):
    def test_loads_role_id_configuration(self) -> None:
        env = {
            "DISCORD_BOT_TOKEN": "token",
            "DISCORD_GUILD_ID": "123",
            "DISCORD_ROLE_ID": "456",
            "DISCORD_ROLE_NAME": "",
        }

        with patch.dict(os.environ, env, clear=True):
            settings = load_settings()

        self.assertEqual(settings.discord_token, "token")
        self.assertEqual(settings.guild_id, 123)
        self.assertEqual(settings.role_id, 456)
        self.assertIsNone(settings.role_name)

    def test_requires_token(self) -> None:
        env = {
            "DISCORD_BOT_TOKEN": "",
            "DISCORD_ROLE_NAME": "Member",
        }

        with patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError):
                load_settings()

    def test_requires_role_selector(self) -> None:
        env = {
            "DISCORD_BOT_TOKEN": "token",
            "DISCORD_ROLE_ID": "",
            "DISCORD_ROLE_NAME": "",
        }

        with patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError):
                load_settings()

    def test_rejects_invalid_integer(self) -> None:
        env = {
            "DISCORD_BOT_TOKEN": "token",
            "DISCORD_ROLE_ID": "abc",
        }

        with patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError):
                load_settings()
