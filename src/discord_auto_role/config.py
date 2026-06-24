from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class Settings:
    discord_token: str
    guild_id: int | None
    role_id: int | None
    role_name: str | None

    @property
    def target_description(self) -> str:
        if self.role_id is not None:
            return f"role ID {self.role_id}"
        return f"role name '{self.role_name}'"


def _read_optional_int(name: str) -> int | None:
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return None

    try:
        return int(raw_value)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer.") from exc


def _read_optional_text(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


def load_settings() -> Settings:
    load_dotenv()

    token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
    guild_id = _read_optional_int("DISCORD_GUILD_ID")
    role_id = _read_optional_int("DISCORD_ROLE_ID")
    role_name = _read_optional_text("DISCORD_ROLE_NAME")

    if not token:
        raise ConfigError("DISCORD_BOT_TOKEN is required.")

    if role_id is None and role_name is None:
        raise ConfigError("Set DISCORD_ROLE_ID or DISCORD_ROLE_NAME.")

    return Settings(
        discord_token=token,
        guild_id=guild_id,
        role_id=role_id,
        role_name=role_name,
    )
