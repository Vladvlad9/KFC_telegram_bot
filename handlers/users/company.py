from aiogram import types

from keyboards.default import user_panel_kb
from loader import dp, db


@dp.message_handler(text="О компании")
async def bot_start(message: types.Message):
    await message.answer(text=f"Добро пожаловать {message.from_user.first_name}!",
                         reply_markup=await user_panel_kb())