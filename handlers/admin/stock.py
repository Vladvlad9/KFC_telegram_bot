from aiogram import types

from keyboards.default import action_KB_admin
from loader import dp


@dp.message_handler(text="Акции_admin")
async def load_name(message: types.Message):
    await message.answer("Произведите действия", reply_markup= await action_KB_admin())