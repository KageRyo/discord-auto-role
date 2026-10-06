from __future__ import annotations

import unittest
from dataclasses import dataclass

from discord_auto_role.role_selector import assignment_problem


@dataclass
class FakeRole:
    id: int
    name: str
    position: int
    assignable: bool

    def is_assignable(self) -> bool:
        return self.assignable


class AssignmentProblemTestCase(unittest.TestCase):
    def test_returns_none_when_role_is_assignable(self) -> None:
        role = FakeRole(id=1, name="Member", position=1, assignable=True)

        self.assertIsNone(assignment_problem(role, can_manage_roles=True))

    def test_reports_missing_manage_roles_permission(self) -> None:
        role = FakeRole(id=1, name="Member", position=1, assignable=True)

        problem = assignment_problem(role, can_manage_roles=False)

        self.assertIn("Manage Roles", problem)

    def test_reports_role_above_bot(self) -> None:
        role = FakeRole(id=1, name="Admin", position=10, assignable=False)

        problem = assignment_problem(role, can_manage_roles=True)

        self.assertIn("Admin", problem)


if __name__ == "__main__":
    unittest.main()
