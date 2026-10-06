from __future__ import annotations

import logging

import discord
from discord import app_commands
from discord.ext import commands

from discord_auto_role.config import Settings
from discord_auto_role.role_selector import assignment_problem, find_target_role

LOGGER = logging.getLogger(__name__)


class AutoRoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.settings: Settings = bot.settings

    def _is_target_guild(self, guild: discord.Guild) -> bool:
        return self.settings.guild_id is None or guild.id == self.settings.guild_id

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if not self._is_target_guild(member.guild):
            return

        # Members still going through Membership Screening / Onboarding are
        # handled in on_member_update once they complete it.
        if member.pending:
            LOGGER.info("Member %s (%s) is pending verification; deferring.", member, member.id)
            return

        await self._assign_role(member)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        if not self._is_target_guild(after.guild):
            return

        if before.pending and not after.pending:
            await self._assign_role(after)

    async def _assign_role(self, member: discord.Member) -> None:
        guild = member.guild
        role = find_target_role(guild.roles, self.settings)
        if role is None:
            LOGGER.warning(
                "Role not found in guild %s using %s.",
                guild.id,
                self.settings.target_description,
            )
            return

        if role in member.roles:
            return

        problem = assignment_problem(
            role,
            can_manage_roles=guild.me.guild_permissions.manage_roles,
        )
        if problem is not None:
            LOGGER.warning("Cannot assign role in guild %s: %s.", guild.id, problem)
            return

        try:
            await member.add_roles(role, reason="Auto role assignment")
        except discord.HTTPException:
            LOGGER.exception(
                "Failed to assign role %s (%s) to %s (%s) in guild %s.",
                role.name,
                role.id,
                member,
                member.id,
                guild.id,
            )
            return

        LOGGER.info(
            "Assigned role %s (%s) to %s (%s) in guild %s.",
            role.name,
            role.id,
            member,
            member.id,
            guild.id,
        )

    @app_commands.command(
        name="autorole",
        description="Show the auto-role configuration and whether the bot can assign it.",
    )
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    @app_commands.default_permissions(manage_roles=True)
    async def autorole_status(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
            return

        if not self._is_target_guild(guild):
            await interaction.response.send_message(
                "Auto role is not enabled for this server.", ephemeral=True
            )
            return

        role = find_target_role(guild.roles, self.settings)
        if role is None:
            status = f"Role not found using {self.settings.target_description}."
        else:
            problem = assignment_problem(
                role,
                can_manage_roles=guild.me.guild_permissions.manage_roles,
            )
            status = f"Cannot assign: {problem}." if problem else "Ready to assign."

        embed = discord.Embed(title="Auto Role", color=discord.Color.blurple())
        embed.add_field(name="Target", value=role.mention if role else "—", inline=False)
        embed.add_field(name="Status", value=status, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
