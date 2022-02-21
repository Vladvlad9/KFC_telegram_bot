from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin import review_inline_keyboard
from loader import dp, db



@dp.message_handler(text="Отзывы о ресторанах_admin")
async def load_name(message: types.Message):
    res = await db.get_all_reviews()
    for i in res:
        await message.answer(f"<b>Имя:</b> {i[2]}\n"
                             f"<b>Ресторан:</b> {i[3]}\n"
                             f"<b>Дата:</b> {i[4]}\n\n"
                             f"<b>Отзыв:</b> <i>{i[5]}\n\n</i>"
                             f"<b>Статус:</b> <i>{i[6]}</i>",
                             parse_mode="HTML", reply_markup= await review_inline_keyboard())