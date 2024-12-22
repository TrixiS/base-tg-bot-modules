from aiogram import F, types

from ... import markups
from ...phrases import phrases
from . import router


@router.message(F.text == phrases.admin.admin)
async def admin_handler(message: types.Message):
    await message.answer(phrases.admin.admin, reply_markup=markups.admin_markup)
