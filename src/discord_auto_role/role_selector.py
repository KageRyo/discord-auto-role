from __future__ import annotations

from typing import Iterable, Protocol, TypeVar

from discord_auto_role.config import Settings


class RoleLike(Protocol):
    id: int
    name: str


class AssignableRole(RoleLike, Protocol):
    position: int

    def is_assignable(self) -> bool: ...


T = TypeVar("T", bound=RoleLike)


def find_target_role(roles: Iterable[T], settings: Settings) -> T | None:
    if settings.role_id is not None:
        for role in roles:
            if role.id == settings.role_id:
                return role

    if settings.role_name is not None:
        for role in roles:
            if role.name == settings.role_name:
                return role

    return None


def assignment_problem(role: AssignableRole, *, can_manage_roles: bool) -> str | None:
    """Return why the bot cannot assign ``role``, or ``None`` if it can."""
    if not can_manage_roles:
        return "the bot is missing the Manage Roles permission"

    if not role.is_assignable():
        return (
            f"role '{role.name}' is managed by an integration or is not below "
            "the bot's highest role"
        )

    return None
