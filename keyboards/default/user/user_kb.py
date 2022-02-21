from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def user_panel_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        row_width=3,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [
                KeyboardButton(text="Рестораны"),
                KeyboardButton(text="Карьера")
            ],
            [
                KeyboardButton(text="О компании"),
            ]
        ]
    )
    return keyboard


async def restaurants_panel_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        row_width=3,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [
                KeyboardButton(text="Меню"),
                KeyboardButton(text="Купоны"),
                KeyboardButton(text="Карьера")
            ],
            [
                KeyboardButton(text="Корзина"),
                KeyboardButton(text="Акции"),
                KeyboardButton(text="Оставить отзыв")
            ],
            [
                KeyboardButton(text="Назад")

            ]
        ]
    )
    return keyboard


