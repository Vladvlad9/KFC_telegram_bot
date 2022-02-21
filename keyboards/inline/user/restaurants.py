from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db


async def restaurants_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        row_width=1
    )
    keyboard.add(*[InlineKeyboardButton(text=restaurants, callback_data=f"restaurants_{restaurants}") for restaurants in
                   await db.get_restaurants()])
    return keyboard


async def menu_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        row_width=2
    )
    keyboard.add(*[InlineKeyboardButton(text=menu, callback_data=f"menu_{menu}") for menu in
                   await db.get_menu()])
    return keyboard


async def get_product_keyboard_inline(price, name_products):
    buttons = [
        types.InlineKeyboardButton(text="-1", callback_data=f'num_decr_{name_products}_{price}'),
        types.InlineKeyboardButton(text="+1", callback_data=f'num_incr_{name_products}_{price}'),
        types.InlineKeyboardButton(text="Изменить состав", callback_data=f'change_{name_products}'),
        InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{name_products}_{price}"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard


async def update_compound_product_keyboard_inline(compound):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for i in compound:
        key = [
            types.InlineKeyboardButton(text=f"Добавить: {i[1]}", callback_data=f'c_s_{i[0]}_{i[1]}'),
            types.InlineKeyboardButton(text=f"Убрать: {i[1]}", callback_data=f'c_p_{i[0]}_{i[1]}'),
        ]
        keyboard.add(*key)
    keyboard.add(InlineKeyboardButton(text=f'Применить изменения: {compound[0][0]}',
                                      callback_data=f"applyCompound_{compound[0][0]}"))

    return keyboard


async def change_product_keyboard_inline():
    buttons = [
        types.InlineKeyboardButton(text="Добавить", callback_data=f'addProd'),
        types.InlineKeyboardButton(text="Убрать", callback_data=f'noAdd'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard



"""Купоны"""
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
        #types.InlineKeyboardButton(text="Изменить состав", callback_data=f'change_{name_products}'),
        InlineKeyboardButton(text="Добавить в корзину", callback_data=f"addCoup_{name_products}_{price}"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    return keyboard
