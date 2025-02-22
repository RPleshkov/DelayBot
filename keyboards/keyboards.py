from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_receipt(id: str):
    button = InlineKeyboardButton(text="Прочитано", callback_data=f"confirm_{id}")
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
