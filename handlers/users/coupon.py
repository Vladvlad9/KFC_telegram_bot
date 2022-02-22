from aiogram import types
from aiogram.dispatcher.filters import Text

from keyboards.default import user_panel_kb
from keyboards.inline.user import restaurants, coupons_inline, get_coupons_keyboard_inline
from loader import dp, db

user_data = {}#пересмотреть

@dp.message_handler(text="Купоны")
async def coupons_start(message: types.Message):
    await message.answer(text=f"Выберите",
                         reply_markup=await coupons_inline())


"""Измененеый вывод купона"""
async def update_num_text(message: types.Message, new_value: int, name_prod, price):
    await message.edit_text(f'<b>Цена:</b>{price}\n\n'
                            f'<b>Количество:</b> {new_value}',
                            reply_markup=await get_coupons_keyboard_inline(price, name_prod),
                            parse_mode="HTML")


"""Первоначальный вывод купона"""
@dp.callback_query_handler(lambda call: "coupons" in call.data)
async def show_coupons(call: types.CallbackQuery):
    counpons = await db.sql_show_coupons()

    markup = types.InlineKeyboardMarkup()
    types.InlineKeyboardMarkup()

    for i in counpons:
        await call.message.answer_photo(i[1], reply_markup=markup)
        await call.message.answer(f'<b>Цена:</b>{i[3]}\n\n',
                                  reply_markup=await get_coupons_keyboard_inline(i[3], i[2]),
                                  parse_mode="HTML")


@dp.callback_query_handler(lambda call: "addCoup" in call.data)
async def coupons_add(call: types.CallbackQuery):
    name_coupons = call.data.split("_")[1]
    price_product = call.data.split("_")[2]

    basket_user = await db.sql_show_basket_product(call.from_user.id, name_coupons)

    if not basket_user:
        await db.sql_add_basket(call.from_user.id, 'Купон ' + name_coupons, 1, price_product, price_product)
        await call.answer(f"Вы успешно добавили Купон {name_coupons} в корзину", show_alert=False)
    else:
        current_count_product_basket_user = basket_user[0][4]
        await db.sql_update_product_basket_user(call.from_user.id, current_count_product_basket_user,
                                                price_product,
                                                price_product)
        await call.answer(f"Вы успешно добавили Купон {name_coupons} в корзину", show_alert=False)


@dp.callback_query_handler(Text(startswith="num_"))
async def callbacks_num(call: types.CallbackQuery):
    user_value = user_data.get(call.from_user.id, 1)
    action = call.data.split("_")[1]
    name_coupons = call.data.split('_')[2]
    price = call.data.split('_')[3]


    current_count_product_basket_user = 0
    basket_user = await db.sql_show_basket_product(call.from_user.id, name_coupons)
    if not basket_user:
        await db.sql_add_basket(call.from_user.id, name_coupons, user_value, price, price)
        basket_user = await db.sql_show_basket_product(call.from_user.id, name_coupons)
        current_count_product_basket_user = basket_user[0][3]
        current_price_basket_user = basket_user[0][4]
    else:
        for i in basket_user:
            for j in i:
                if j == name_coupons:
                    current_count_product_basket_user = i[3]
                    current_price_basket_user = i[4]
                    total_amount = i[5]
                    break


    if action == "incr":
        current_count_product_basket_user += 1
        res_price = float(current_price_basket_user) * current_count_product_basket_user
        await update_num_text(call.message, current_count_product_basket_user, name_coupons, res_price)
        await db.sql_update_product_basket_user(call.from_user.id, current_count_product_basket_user, res_price,
                                                name_coupons)

    elif action == "decr":
        current_count_product_basket_user -= 1
        if current_count_product_basket_user >= 1:
            res_price = float(total_amount) - float(current_price_basket_user)
            await update_num_text(call.message, current_count_product_basket_user, name_coupons, res_price)
            await db.sql_update_product_basket_user(call.from_user.id, current_count_product_basket_user, res_price,
                                                    name_coupons)
        else:
            await call.answer("Должна быть одна позиция", show_alert=False)