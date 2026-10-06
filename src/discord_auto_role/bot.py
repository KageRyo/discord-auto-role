from __future__ import annotations

import logging

import discord
from discord.ext import commands

from discord_auto_role.cogs.auto_role import AutoRoleCog
from discord_auto_role.config import load_settings
from discord_auto_role.logging_config import configure_logging

LOGGER = logging.getLogger(__name__)

# This bot never joins voice channels, so skip the optional voice dependency warnings.
discord.VoiceClient.warn_nacl = False
discord.VoiceClient.warn_dave = False


class AutoRoleBot(commands.Bot):
    def __init__(self) -> None:
        # Only request what auto-role needs: guild/role cache and the
        # privileged Server Members intent for join/update events.
        intents = discord.Intents.none()
        intents.guilds = True
        intents.members = True

        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            activity=discord.CustomActivity(name="Assigning roles to new members"),
            allowed_mentions=discord.AllowedMentions.none(),
        )
        self.settings = load_settings()

    async def setup_hook(self) -> None:
        await self.add_cog(AutoRoleCog(self))

    async def on_ready(self) -> None:
        if self.user is None:
            return

        LOGGER.info(
            "Logged in as %s (%s) in %d guild(s).",
            self.user,
            self.user.id,
            len(self.guilds),
        )


def run() -> None:
    configure_logging()
    bot = AutoRoleBot()
    LOGGER.info("Starting bot with target %s", bot.settings.target_description)
    bot.run(bot.settings.discord_token, log_handler=None)
