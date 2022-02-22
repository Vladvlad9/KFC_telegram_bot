from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_coupons_keyboard_inline(price, name_сoupons):
    buttons = [
        types.InlineKeyboardButton(text="-1", callback_data=f'num_decr_{name_сoupons}_{price}'),
        types.InlineKeyboardButton(text="+1", callback_data=f'num_incr_{name_сoupons}_{price}'),
        InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{name_сoupons}_{price}"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard