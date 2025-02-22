from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def trash_messages(msg: Message):
    await msg.answer(text="Ничего тебе не могу сказать по этому поводу.")
