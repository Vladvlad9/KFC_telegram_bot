from aiogram import types

from keyboards.default import user_panel_kb
from keyboards.inline.user import restaurants, coupons_inline
from loader import dp, db


@dp.message_handler(text="Купоны")
async def coupons_start(message: types.Message):
    await message.answer(text=f"Выберите",
                         reply_markup=await coupons_inline())


"""Измененеый вывод купона"""
async def update_num_text(message: types.Message, new_value: int, name_prod, price):
    await message.edit_text(f'<b>Цена:</b>{price}\n\n'
                            f'<b>Количество:</b> {new_value}',
                            reply_markup=await restaurants.get_product_keyboard_inline(price, name_prod),
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
                                  reply_markup=await restaurants.get_coupons_keyboard_inline(i[2], i[3]),
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