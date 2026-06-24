from __future__ import annotations

import unittest
from dataclasses import dataclass

from discord_auto_role.config import Settings
from discord_auto_role.role_selector import find_target_role


@dataclass
class FakeRole:
    id: int
    name: str


class FindTargetRoleTestCase(unittest.TestCase):
    def test_finds_role_by_id(self) -> None:
        settings = Settings(
            discord_token="token",
            guild_id=None,
            role_id=2,
            role_name=None,
        )
        roles = [FakeRole(id=1, name="Member"), FakeRole(id=2, name="Visitor")]

        role = find_target_role(roles, settings)

        self.assertIsNotNone(role)
        self.assertEqual(role.id, 2)

    def test_finds_role_by_name(self) -> None:
        settings = Settings(
            discord_token="token",
            guild_id=None,
            role_id=None,
            role_name="Member",
        )
        roles = [FakeRole(id=1, name="Member"), FakeRole(id=2, name="Visitor")]

        role = find_target_role(roles, settings)

        self.assertIsNotNone(role)
        self.assertEqual(role.name, "Member")

    def test_returns_none_when_role_is_missing(self) -> None:
        settings = Settings(
            discord_token="token",
            guild_id=None,
            role_id=99,
            role_name=None,
        )
        roles = [FakeRole(id=1, name="Member")]

        role = find_target_role(roles, settings)

        self.assertIsNone(role)
