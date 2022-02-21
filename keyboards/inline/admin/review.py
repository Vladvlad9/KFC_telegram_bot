from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db


async def review_inline_keyboard() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        row_width=2
    )
    keyboard.add(*[InlineKeyboardButton(text="Обработать", callback_data=f"id_review_{id_review}") for id_review in
                   await db.get_id_review()])
    return keyboard