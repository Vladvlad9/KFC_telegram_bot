from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from loader import dp, bot, db
from keyboards.default import action_KB_admin
from keyboards.default.admin import admin_kb

ID = None


class FSMCoupouns(StatesGroup):
    photo = State()
    name = State()
    price = State()


@dp.message_handler(text="Купоны_admin")
async def load_name(message: types.Message):
    await message.answer("Заполни анкету и присоединяйся к нашей команде", reply_markup=await action_KB_admin())


@dp.message_handler(text="Добавить", state=None)
async def cm_start_coupons(message: types.Message):
    await FSMCoupouns.photo.set()
    await message.reply('Загрузить фото')


@dp.message_handler(content_types=['photo'], state=FSMCoupouns.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMCoupouns.next()
    await message.reply("Введи Номер Купона")


@dp.message_handler(state=FSMCoupouns.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await FSMCoupouns.next()
        await message.reply("Введите Цену")


@dp.message_handler(state=FSMCoupouns.price)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    res = data.values()
    r = list(res)
    img = r[0]
    name = r[1]
    price = r[2]

    await db.sql_add_coupons(img, name, price)
    await state.finish()