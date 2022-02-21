from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text

from keyboards.default.admin import admin_kb
from keyboards.default.user.user_kb import user_panel_kb
from loader import dp, db

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(text=f"Добро пожаловать {message.from_user.first_name}!",
                         reply_markup=await user_panel_kb())


@dp.message_handler(commands=["create_database", "create_db", ])
async def create_database(message: types.Message):
    await message.answer(text="База данных успешно создана!")
    await db.create_all_database()


@dp.message_handler(commands=["moderator", "admin", ])
async def create_database(message: types.Message):
    await message.answer(text="Вы вошли как админ", reply_markup=await admin_kb.start_kb_admin())



















