from __future__ import annotations

import logging

import discord
from discord.ext import commands

from discord_auto_role.cogs.auto_role import AutoRoleCog
from discord_auto_role.config import load_settings
from discord_auto_role.logging_config import configure_logging

LOGGER = logging.getLogger(__name__)


class AutoRoleBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            activity=discord.Game(name="Auto Role"),
        )
        self.settings = load_settings()

    async def setup_hook(self) -> None:
        await self.add_cog(AutoRoleCog(self))

    async def on_ready(self) -> None:
        if self.user is None:
            return

        LOGGER.info("Logged in as %s (%s)", self.user, self.user.id)


def run() -> None:
    configure_logging()
    bot = AutoRoleBot()
    LOGGER.info("Starting bot with target %s", bot.settings.target_description)
    bot.run(bot.settings.discord_token, log_handler=None)
