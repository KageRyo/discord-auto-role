from __future__ import annotations

from typing import Any, Iterable

CommandSignature = tuple[str, str, int | None]


def _permissions_value(permissions: Any) -> int | None:
    return None if permissions is None else permissions.value


def local_signature(command: Any) -> CommandSignature:
    """Signature of a command registered on the local CommandTree."""
    return (
        command.name,
        getattr(command, "description", ""),
        _permissions_value(getattr(command, "default_permissions", None)),
    )


def remote_signature(command: Any) -> CommandSignature:
    """Signature of an AppCommand fetched from Discord."""
    return (
        command.name,
        command.description,
        _permissions_value(command.default_member_permissions),
    )


def commands_match(local: Iterable[Any], remote: Iterable[Any]) -> bool:
    """Return True when the local and remote command sets look identical.

    Only names, descriptions and default permissions are compared, which is
    enough to skip redundant syncs on restart. Changing a command's options
    alone is not detected; bump its description or sync manually in that case.
    """
    return sorted(map(local_signature, local)) == sorted(map(remote_signature, remote))
