from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def confirm_order_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        row_width=1
    )
    keyboard.add(*[InlineKeyboardButton(text="Оплатить", callback_data=f"confirm_")])
    keyboard.add(*[InlineKeyboardButton(text="Редактировать товар", callback_data=f"del_")])
    return keyboard


async def delete_prod_inline_keyboard(name_prod) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        row_width=1
    )
    keyboard.add(*[InlineKeyboardButton(text="Удалить", callback_data=f"delProd_{name_prod}")])
    return keyboard