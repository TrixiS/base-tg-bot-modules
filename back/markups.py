back_button = KeyboardButton(text=phrases.back_button_text)
back_markup = (
    ReplyKeyboardBuilder()
    .add(back_button)
    .as_markup(resize_keyboard=True, one_time_keyboard=False, is_persistent=True)
)
