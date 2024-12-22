from typing import Any, Awaitable, Callable

from aiogram import types

from .. import filters


def admin_middleware(
    handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
    update: types.TelegramObject,
    data: dict[str, Any],
) -> Any:
    from_user: types.User | None = getattr(update, "from_user", None)

    if from_user is None:
        raise TypeError(f"{update.__class__.__name__} has no 'from_user' attribute")

    data["is_admin"] = filters.is_admin(from_user.id)
    return handler(update, data)
