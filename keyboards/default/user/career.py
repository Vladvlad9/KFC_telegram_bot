from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def career_panel_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [
                KeyboardButton(text="О Вакансии"),
                KeyboardButton(text="Хочу работать")
            ],
            [
                KeyboardButton(text="Назад")
            ]
        ]
    )
    return keyboard