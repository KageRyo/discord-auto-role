from __future__ import annotations

import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from discord_auto_role.cogs.auto_role import AutoRoleCog
from discord_auto_role.command_sync import commands_match
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
        await self._sync_app_commands()

    async def _sync_app_commands(self) -> None:
        if self.settings.guild_id is not None:
            # Guild-scoped sync is applied instantly, which suits a single-server bot.
            guild = discord.Object(id=self.settings.guild_id)
            self.tree.copy_global_to(guild=guild)
            await self._sync_if_changed(guild)
            # Drop global copies left over from running without DISCORD_GUILD_ID,
            # otherwise every command would show up twice in that guild.
            self.tree.clear_commands(guild=None)
            await self._sync_if_changed(None)
            return

        await self._sync_if_changed(None)
        # Drop guild-scoped copies left over from a previous DISCORD_GUILD_ID setup.
        async for guild in self.fetch_guilds(limit=None):
            await self._sync_if_changed(guild)

    async def _sync_if_changed(self, guild: discord.abc.Snowflake | None) -> None:
        scope = "global scope" if guild is None else f"guild {guild.id}"
        remote = await self.tree.fetch_commands(guild=guild)
        local = self.tree.get_commands(guild=guild)
        if commands_match(local, remote):
            LOGGER.info("App commands for %s are up to date; skipping sync.", scope)
            return

        synced = await self.tree.sync(guild=guild)
        LOGGER.info("Synced %d app command(s) to %s.", len(synced), scope)

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
    load_dotenv()
    bot = AutoRoleBot()
    LOGGER.info("Starting bot with target %s", bot.settings.target_description)
    bot.run(bot.settings.discord_token, log_handler=None)
