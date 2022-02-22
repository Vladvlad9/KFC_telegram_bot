from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def coupons_inline():
    keyboard = InlineKeyboardMarkup(
        row_width=1
    )
    keyboard.add(*[InlineKeyboardButton(text="Просмотреть", callback_data=f"coupons")])
    return keyboard


async def get_coupons_keyboard_inline(name_products, price):
    buttons = [
        types.InlineKeyboardButton(text="-1", callback_data=f'coup_decr_{name_products}_{price}'),
        types.InlineKeyboardButton(text="+1", callback_data=f'coup_incr_{name_products}_{price}'),
        InlineKeyboardButton(text="Добавить в корзину", callback_data=f"addCoup_{name_products}_{price}"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard