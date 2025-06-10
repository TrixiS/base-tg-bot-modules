from .config import config


def is_admin(user_id: int):
    return user_id in config.admin_user_ids


def admin_filter(_, is_admin: bool):
    return is_admin
