from __future__ import annotations

from typing import Iterable, Protocol, TypeVar

from discord_auto_role.config import Settings


class RoleLike(Protocol):
    id: int
    name: str


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
