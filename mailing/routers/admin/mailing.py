import asyncio

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram3_form import Form, FormField

from ... import markups
from ...callback_data import CancelMailingCallbackData
from ...client import bot
from ...database.models import BotUser
from ...phrases import phrases
from . import router

_MAILING_TASKS_MAP: dict[tuple[int, int], asyncio.Task] = {}


class MailingForm(Form):
    message: types.Message = FormField(
        enter_message_text=phrases.admin.enter_mailing_message_message_text,
        reply_markup=markups.back_markup,
    )


@MailingForm.submit(router=router)
async def mailing_form_submit_handler(form: MailingForm):
    task_key = (form.chat_id, form.message.message_id)
    _MAILING_TASKS_MAP[task_key] = asyncio.current_task()  # type: ignore

    await form.answer(phrases.admin.mailing_message_text)  # TODO: set reply markup here

    bot_user_ids: list[int] = await BotUser.filter().values_list(  # type: ignore
        "id",
        flat=True,
    )

    startup_message = await form.answer(
        phrases.admin.mailing_startup_message_text_fmt.format(
            bot_users_count=len(bot_user_ids)
        ),
        reply_markup=markups.create_cancel_mailing_markup(form.message.message_id),
    )

    mailed_messages_count = 0

    await asyncio.sleep(5)

    for bot_user_id in bot_user_ids:
        try:
            await form.message.copy_to(bot_user_id)
        except Exception:
            continue

        mailed_messages_count += 1

    await startup_message.delete()
    await form.answer(
        phrases.admin.mailed_messages_count_message_text_fmt.format(
            mailed_messages_count=mailed_messages_count,
            bot_users_count=len(bot_user_ids),
        )
    )

    del _MAILING_TASKS_MAP[task_key]


@router.message(F.text == phrases.admin.mailing_button_text)
async def mailing_handler(_: types.Message, state: FSMContext):
    await MailingForm.start(bot, state)


@router.callback_query(CancelMailingCallbackData.filter())
async def cancel_mailing_handler(
    query: types.CallbackQuery, callback_data: CancelMailingCallbackData
):
    task_key = (query.from_user.id, callback_data.message_id)
    task = _MAILING_TASKS_MAP.get(task_key)

    if task is not None:
        task.cancel()
        del _MAILING_TASKS_MAP[task_key]

    await query.answer(phrases.admin.mailing_cancelled_message_text, show_alert=True)
    await query.message.delete()  # type: ignore
