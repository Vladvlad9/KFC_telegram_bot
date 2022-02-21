
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMreview(StatesGroup):
    name_user = State()
    restaurant = State()
    description = State()


@dp.message_handler(text="Оставить отзыв")
async def load_name(message: types.Message):
    await message.answer("Напишите о вашей проблеме или о чем нибудь хорошем")
    await FSMreview.next()
    await message.reply("Введи имя")


@dp.message_handler(state=FSMreview.name_user)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_user'] = message.text
    await FSMreview.next()
    await message.reply("Введи ресторан")


@dp.message_handler(state=FSMreview.restaurant)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['restaurant'] = message.text
    await FSMreview.next()
    await message.reply("Опишите вашу проблему")


@dp.message_handler(state=FSMreview.description)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    review = data.values()
    result_review = list(review)

    user_id = message.from_user.id
    name_user = result_review[0]
    restaurant = result_review[1]
    current_time_date = datetime.now()
    description = result_review[2]
    status = "Не обработан"

    await db.sql_add_review(user_id, name_user, restaurant, current_time_date, description, status)
    await message.answer("Спасибо, ваш отзыв полезен о нас")

    await state.finish()