user_start_markup = (
    ReplyKeyboardBuilder()
    .adjust(2, repeat=True)
    .as_markup(resize_keyboard=True, one_time_keyboard=False, is_persistent=True)
)

admin_start_markup = (
    ReplyKeyboardBuilder.from_markup(user_start_markup)
    .button(text=phrases.admin.admin)
    .adjust(2, repeat=True)
    .as_markup(resize_keyboard=True, one_time_keyboard=False, is_persistent=True)
)


def get_start_markup(is_admin: bool):
    if is_admin:
        return admin_start_markup

    return user_start_markup
