from aiogram import types
from aiogram.dispatcher.filters import Text

from keyboards.default import user_panel_kb
from keyboards.inline.user import restaurants, change_product_keyboard_inline
from keyboards.default.user import user_kb
from loader import dp, db

count = 1


@dp.message_handler(text="Назад")
async def bot_start(message: types.Message):
    await message.answer(text=f"Добро пожаловать {message.from_user.first_name}!",
                         reply_markup=await user_panel_kb())


@dp.message_handler(text="Рестораны")
async def catalog(message: types.Message):
    await message.answer(
        text="Выберите ресторан!",
        reply_markup=await restaurants.restaurants_inline_keyboard()
    )


@dp.callback_query_handler(lambda call: "restaurants_" in call.data)
async def get_category(call: types.CallbackQuery):
    name_restaraunt = call.data.split("_")[1]
    await call.message.answer(f"Вы перешли в ресторан: {name_restaraunt}\n\nВыберите из списка позицию:",
                              reply_markup=await user_kb.restaurants_panel_kb())
    action_restaurants = await db.sql_show_user_action_name_restaurant(call.from_user.id)
    if not action_restaurants:
        await db.sql_action_user(call.from_user.id, name_restaraunt, 'null')
    else:
        await db.sql_update_action_user_restaraunt(call.from_user.id, name_restaraunt)


@dp.message_handler(text="Меню")
async def catalog(message: types.Message):
    await message.answer(
        text="Выберите позицию из меню!",
        reply_markup=await restaurants.menu_inline_keyboard()
    )




user_data = {}


async def update_num_text(message: types.Message, new_value: int, name_prod, description, price):
    await message.edit_text(f'<b>Название:</b> {name_prod}\n\n'
                            f'<b>Описание:</b>{description}\n\n'
                            f'<b>Цена:</b>{price}\n\n'
                            f'<b>Количество:</b> {new_value}',
                            reply_markup=await restaurants.get_product_keyboard_inline(price, name_prod),
                            parse_mode="HTML")


async def update_compound(message: types.Message, new_value: int, name_prod, description, price, compound):
    txt = ''
    new_data = []
    for i in compound:
        txt += f"{i[1]} - {i[2]}\n"
        data = []
        data.append(i[0])
        data.append(i[1])
        new_data.append(data)

    await message.edit_text(f'<b>Название:</b> {name_prod}\n\n'
                            f'<b>Описание:</b>{description}\n\n'
                            f'<b>Цена:</b>{price}\n\n'
                            f'<b>Количество:</b> {new_value}\n\n'
                            f'Состав:\n{txt}',
                            reply_markup=await restaurants.update_compound_product_keyboard_inline(compound),
                            parse_mode="HTML")


async def new_update_compound(message: types.Message, new_value: int, name_prod, description, price, compound):
    txt = ''
    for i in compound:
        if i[4] == 'null':
            txt += f"{i[1]} - {i[2]}\n"
        else:
            txt += f"{i[1]} - {i[4]}\n"
    await message.edit_text(f'<b>Название:</b> {name_prod}\n\n'
                            f'<b>Описание:</b>{description}\n\n'
                            f'<b>Цена:</b>{price}\n\n'
                            f'<b>Количество:</b> {new_value}\n\n'
                            f'Состав:\n{txt}',
                            reply_markup=await restaurants.update_compound_product_keyboard_inline(compound),
                            parse_mode="HTML")


"""Первоначальный вывод продукта"""
@dp.callback_query_handler(lambda call: "menu_" in call.data)
async def get_product(call: types.CallbackQuery):
    print(call.data)
    subcategory = call.data.split("_")[1]
    english_name_menu = await db.get_English_name_menu(subcategory)
    product = await db.get_menu_product(english_name_menu)

    await db.sql_update_action_user(call.from_user.id, english_name_menu)

    markup = types.InlineKeyboardMarkup()
    types.InlineKeyboardMarkup()
    for i in product:
        await call.message.answer_photo(i[1], reply_markup=markup)
        await call.message.answer(f'<b>Название:</b> {i[2]}\n\n'
                                  f'<b>Описание:</b>{i[3]}\n\n'
                                  f'<b>Цена:</b>{i[4]}\n\n',
                                  reply_markup=await restaurants.get_product_keyboard_inline(i[4], i[2]),
                                  parse_mode="HTML")


"""Добавление в корзину одного продукта"""
@dp.callback_query_handler(lambda call: "add_" in call.data)
async def add_product_to_cart(call: types.CallbackQuery):
    name_user = call.from_user.id
    name_product = call.data.split("_")[1]
    price_product = call.data.split("_")[2]

    basket_user = await db.sql_show_basket_product(call.from_user.id, name_product)
    new_price = 0
    if not basket_user:
        await db.sql_add_basket(name_user, name_product, count, price_product, price_product)
        await call.answer(f"Вы успешно добавили {name_product} в корзину", show_alert=False)
    else:
        current_count_product_basket_user = basket_user[0][4]
        await db.sql_update_product_basket_user(call.from_user.id, current_count_product_basket_user,
                                                price_product,
                                                price_product)
        await call.answer(f"Вы успешно добавили {name_product} в корзину", show_alert=False)


@dp.callback_query_handler(lambda call: "change_" in call.data)
async def change_product(call: types.CallbackQuery):
    name_product = call.data.split("_")[1]

    new_compound = await db.sql_new_user_compound(call.from_user.id, name_product)
    if not new_compound:
        current_compaund = await db.sql_compound(str(name_product))
    else:
        current_compaund = new_compound

    user_basket = await db.sql_show_basket(call.from_user.id)
    table = await db.sql_show_user_action_name_name_menu(call.from_user.id)
    product = await db.get_current_product(table[0], name_product)
    count = 0
    if not user_basket:
        count = 1
        cur_price = product[0][4]
    else:
        count = user_basket[0][3]
        cur_price = user_basket[0][5]

    await update_compound(call.message, count, name_product, product[0][3], cur_price, current_compaund)


@dp.callback_query_handler(Text(startswith="num_"))
async def callbacks_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 1)
    action = call.data.split("_")[1]
    name_prod = call.data.split('_')[2]
    price = call.data.split('_')[3]
    user_id = call.from_user.id

    curent_table = await db.sql_show_user_action_name_name_menu(call.from_user.id)
    current_product = await db.get_current_product(curent_table[0], name_prod)

    current_count_product_basket_user = 0

    basket_user = await db.sql_show_basket_product(call.from_user.id, name_prod)
    if not basket_user:
        await db.sql_add_basket(user_id, name_prod, user_value, price, price)
        basket_user = await db.sql_show_basket_product(call.from_user.id, name_prod)
        current_count_product_basket_user = basket_user[0][3]
        current_price_basket_user = basket_user[0][4]
    else:
        for i in basket_user:
            for j in i:
                if j == name_prod:
                    current_count_product_basket_user = i[3]
                    current_price_basket_user = i[4]
                    total_amount = i[5]
                    break

    if action == "incr":
        current_count_product_basket_user += 1
        res_price = float(current_price_basket_user) * current_count_product_basket_user
        await update_num_text(call.message, current_count_product_basket_user, name_prod, current_product[0][3],
                              res_price)
        await db.sql_update_product_basket_user(call.from_user.id, current_count_product_basket_user, res_price,
                                                name_prod)

    elif action == "decr":
        current_count_product_basket_user -= 1
        if current_count_product_basket_user >= 1:
            res_price = float(total_amount) - float(current_price_basket_user)
            await update_num_text(call.message, current_count_product_basket_user, name_prod, current_product[0][3],
                                  res_price)
            await db.sql_update_product_basket_user(call.from_user.id, current_count_product_basket_user, res_price,
                                                    name_prod)
        else:
            await call.answer("Должна быть одна позиция", show_alert=False)

    elif action == "finish":
        await call.message.edit_text(f"Итого: {user_value}")
    await call.answer()


@dp.callback_query_handler(lambda call: "c_" in call.data)
async def callbacks_Compound(call: types.CallbackQuery):
    action = call.data.split("_")[1]
    name_product = call.data.split("_")[2]
    name_compound = call.data.split("_")[3]


    compound = await db.sql_compound(str(name_product))
    examination = await db.sql_examination_user_compound(call.from_user.id, name_product)

    if not examination:
        for i in compound:
            data_count = str(i[2]).split(' ')
            if data_count[0].isdigit():
                await db.sql_user_compound(call.from_user.id, name_product, i[1], i[2], int(data_count[0]), 'null')
                _count = await db.sql_count_user_compound(call.from_user.id, name_compound, name_product)
    else:
        _count = await db.sql_count_user_compound(call.from_user.id, name_compound, name_product)

    user_basket = await db.sql_show_basket(call.from_user.id)
    table = await db.sql_show_user_action_name_name_menu(call.from_user.id)
    product = await db.get_current_product(table[0], name_product)

    count = 0
    cur_price = 0

    if not user_basket:
        count += 1
        cur_price = product[0][4]
    else:
        count = user_basket[0][3]
        cur_price = user_basket[0][5]

    if action == 'p':#Удаление из состава
        data_count = str(_count[0]).split(' ')

        update_count = str(data_count[0])
        word = str(data_count[1])

        c = ''
        full_world = ''

        for i in update_count:
            if i.isdigit():
                c += i

        for i in word:
            if i.isalpha():
                full_world += i
        NC = await db.sql_new_user_compound(call.from_user.id, name_product)
        upd_count = 0
        coment_compound_put = ''
        for i in NC:
            if i[1] == name_compound:
                upd_count = int(c) - int(i[3])
                coment_compound_put = i[4]
                break

        if upd_count == 0:
            await call.answer(f'{name_compound} больше нету в ващей булочке', show_alert=False)
            if coment_compound_put == 'null':
                comment = f'Без {name_compound}а'
                await db.sql_update_user_compound(call.from_user.id, name_product, name_compound, comment)
                new_compound = await db.sql_new_user_compound(call.from_user.id, name_product)
                await db.sql_update_count_user_compound(call.from_user.id, name_product, name_compound,
                                                        str(upd_count) + ' ' + full_world)

                await new_update_compound(call.message, count, name_product, product[0][3], cur_price, new_compound)
        else:
            if coment_compound_put == 'null':
                await db.sql_update_count_user_compound(call.from_user.id, name_product, name_compound,
                                                        str(upd_count) + ' ' + full_world)
                new_compound = await db.sql_new_user_compound(call.from_user.id, name_product)
                await new_update_compound(call.message, count, name_product, product[0][3], cur_price, new_compound)

    if action == 's':#Добавлние в составе
        #a = examination

        if not examination:
            data_count = str(i[2]).split(' ')
            if data_count[0].isdigit():
                await db.sql_user_compound(call.from_user.id, name_product, i[1], i[2], int(data_count[0]), 'null')
                _count = await db.sql_count_user_compound(call.from_user.id, name_compound, name_product)
        else:
            _count = await db.sql_count_user_compound(call.from_user.id, name_compound, name_product)

        data_count = str(_count[0]).split(' ')

        update_count = str(data_count[0])
        word = str(data_count[1])

        c = ''
        full_world = ''

        for i in update_count:
            if i.isdigit():
                c += i

        for i in word:
            if i.isalpha():
                full_world += i

        new_compound = await db.sql_new_user_compound(call.from_user.id, name_product)
        coment_compound = ""
        upd_count = 0
        for i in new_compound:
            if i[1] == name_compound:
                upd_count = int(c) + int(i[3])
                coment_compound = i[4]
                break

        if coment_compound != 'null':

            await db.sql_update_user_compound(call.from_user.id, name_product, name_compound, 'null')
            await db.sql_update_count_user_compound(call.from_user.id, name_product, name_compound,
                                                    str(upd_count) + ' ' + full_world)
            new_compound = await db.sql_new_user_compound(call.from_user.id, name_product)
            await new_update_compound(call.message, count, name_product, product[0][3], cur_price, new_compound)
        else:
            str_update_count = str(upd_count) + ' ' + full_world
            await db.sql_update_count_user_compound(call.from_user.id, name_product, name_compound,
                                                    str(upd_count) + ' ' + full_world)
            new_compound = await db.sql_new_user_compound(call.from_user.id, name_product)
            await new_update_compound(call.message, count, name_product, product[0][3], cur_price, new_compound)

        print('as')


"""Применить изменения кнопка"""
@dp.callback_query_handler(lambda call: "applyCompound_" in call.data)
async def applyCompound(call: types.CallbackQuery):
    name_product = call.data.split("_")[1]

    # user_basket = await db.sql_show_basket(call.from_user.id)
    table = await db.sql_show_user_action_name_name_menu(call.from_user.id)
    product = await db.get_current_product(table[0], name_product)

    basket_user = await db.sql_show_basket_product(call.from_user.id, name_product)
    if not basket_user:
        await update_num_text(call.message, 1, name_product, product[0][3], product[0][4])
    else:
        await update_num_text(call.message, basket_user[0][3], basket_user[0][2], product[0][3], basket_user[0][5])
