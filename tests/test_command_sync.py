from __future__ import annotations

import unittest
from dataclasses import dataclass

import discord

from discord_auto_role.command_sync import commands_match


@dataclass
class FakeLocalCommand:
    name: str
    description: str
    default_permissions: discord.Permissions | None = None


@dataclass
class FakeRemoteCommand:
    name: str
    description: str
    default_member_permissions: discord.Permissions | None = None


class CommandsMatchTestCase(unittest.TestCase):
    def test_matches_identical_commands_in_any_order(self) -> None:
        perms = discord.Permissions(manage_roles=True)
        local = [
            FakeLocalCommand("autorole", "Show status", perms),
            FakeLocalCommand("ping", "Pong"),
        ]
        remote = [
            FakeRemoteCommand("ping", "Pong"),
            FakeRemoteCommand("autorole", "Show status", discord.Permissions(manage_roles=True)),
        ]

        self.assertTrue(commands_match(local, remote))

    def test_detects_changed_description(self) -> None:
        local = [FakeLocalCommand("autorole", "New description")]
        remote = [FakeRemoteCommand("autorole", "Old description")]

        self.assertFalse(commands_match(local, remote))

    def test_detects_changed_default_permissions(self) -> None:
        local = [FakeLocalCommand("autorole", "Show status", discord.Permissions(manage_roles=True))]
        remote = [FakeRemoteCommand("autorole", "Show status")]

        self.assertFalse(commands_match(local, remote))

    def test_detects_stale_remote_commands(self) -> None:
        remote = [FakeRemoteCommand("autorole", "Show status")]

        self.assertFalse(commands_match([], remote))

    def test_empty_sets_match(self) -> None:
        self.assertTrue(commands_match([], []))


if __name__ == "__main__":
    unittest.main()
