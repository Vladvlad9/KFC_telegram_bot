from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



async def start_kb_admin():
    keyboard = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [
                KeyboardButton(text='Купоны_admin'),
                KeyboardButton(text='Акции_admin')
            ],
            [
                KeyboardButton(text='Меню_admin'),
                KeyboardButton(text='Отзывы о ресторанах_admin')
            ]
        ]
    )
    return keyboard


async def action_KB_admin():
    keyboard = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [
                KeyboardButton(text='Изменить'),
                KeyboardButton(text='Добавить')
            ],
            [
                KeyboardButton(text='Удалить')
            ],
            [
                KeyboardButton(text="Назад")
            ]
        ]
    )
    return keyboard