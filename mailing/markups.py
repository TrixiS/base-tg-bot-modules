def create_cancel_mailing_markup(message_id: int):
    return (
        InlineKeyboardBuilder()
        .button(
            text=phrases.admin.cancel_mailing_button_text,
            callback_data=CancelMailingCallbackData(message_id=message_id),
        )
        .as_markup()
    )
