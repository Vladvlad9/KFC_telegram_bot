from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default import career_panel_kb, user_panel_kb
from loader import dp, db
from aiogram.dispatcher.filters.state import State, StatesGroup

subway = ['Уру́чье','Восто́к','Акаде́мия нау́к','Пло́щадь Яку́ба Ко́ласа']

class FSMcareer(StatesGroup):
    lname = State()
    fname = State()
    age = State()
    phone = State()

    e_mail = State()
    city = State()
    subway = State()
    restaurant = State()


@dp.message_handler(text="Карьера")
async def load_name(message: types.Message):
    await message.answer("Заполни анкету и присоединяйся к нашей команде", reply_markup= await career_panel_kb())


@dp.message_handler(text="Назад")
async def load_name(message: types.Message):
    await message.answer(text=f"Добро пожаловать {message.from_user.first_name}!",
                         reply_markup=await user_panel_kb())


@dp.message_handler(text="Хочу работать")
async def load_name(message: types.Message):
    await FSMcareer.next()
    await message.reply("Введи имя")


@dp.message_handler(state=FSMcareer.lname)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lname'] = message.text
    await FSMcareer.next()
    await message.reply("Введи Фамилию")


@dp.message_handler(state=FSMcareer.fname)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fname'] = message.text
    await FSMcareer.next()
    await message.reply("Введи Возраст")


@dp.message_handler(state=FSMcareer.age)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if int(message.text) < 18:
            await message.reply("У вас не подходящий возраст для работы")
            await state.finish()
        else:
            data['age'] = message.text
            await FSMcareer.next()
            await message.reply("Введи ваш контактный телефон")





@dp.message_handler(state=FSMcareer.phone)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await FSMcareer.next()
    await message.reply("Введи ваш e-mail")


@dp.message_handler(state=FSMcareer.e_mail)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['e_mail'] = message.text
    await FSMcareer.next()
    await message.reply("Введи ваш Город")


@dp.message_handler(state=FSMcareer.city)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await FSMcareer.next()
    await message.reply("Введи ближайшее для вас метро")


@dp.message_handler(state=FSMcareer.subway)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subway'] = message.text
    await FSMcareer.next()
    await message.reply("Введи подходящий для вас ресторан")


@dp.message_handler(state=FSMcareer.restaurant)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['restaurant'] = message.text

    res = data.values()
    r = list(res)
    user_id = message.from_user.id
    lname = r[0]
    fname = r[1]
    age = r[2]
    phone = r[3]

    e_mail = r[4]
    city = r[5]
    subway = r[6]
    restaurant = r[7]

    show_user_id = list(await db.sql_user_id(user_id))

    for i in show_user_id:
        if user_id in i:
            await message.answer("Вы уже подовали заявку, ожидайте звонка")
        else:
            await db.sql_add_user_career(user_id, lname, fname, age, phone, e_mail, city, subway, restaurant)
            await message.answer("Ожидайте звонка мы вам обязательно перезвоним")


    await state.finish()
