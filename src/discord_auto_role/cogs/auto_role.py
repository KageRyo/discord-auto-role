from __future__ import annotations

import logging

import discord
from discord.ext import commands

from discord_auto_role.config import Settings
from discord_auto_role.role_selector import find_target_role

LOGGER = logging.getLogger(__name__)


class AutoRoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.settings: Settings = bot.settings

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if self.settings.guild_id is not None and member.guild.id != self.settings.guild_id:
            return

        role = find_target_role(member.guild.roles, self.settings)
        if role is None:
            LOGGER.warning(
                "Role not found in guild %s using %s.",
                member.guild.id,
                self.settings.target_description,
            )
            return

        await member.add_roles(role, reason="Auto role assignment")
        LOGGER.info(
            "Assigned role %s (%s) to %s (%s) in guild %s.",
            role.name,
            role.id,
            member,
            member.id,
            member.guild.id,
        )
