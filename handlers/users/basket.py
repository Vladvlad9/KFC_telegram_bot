from aiogram import types

from keyboards.inline.user import restaurants, confirm_order_inline_keyboard, delete_prod_inline_keyboard
from loader import dp, db


@dp.message_handler(text="Корзина")
async def catalog(message: types.Message):
    res = await db.sql_show_basket(message.from_user.id)
    production = []
    if res != '':
        for i in res:
            production.append(i[2])

    all_name_prod = await db.sql_user_nameProd_Com_user_compound(message.from_user.id)
    sum = 0
    text = ''

    if not all_name_prod:
        for i in res:
            sum += float(i[5])
            text += f'''<b>Название:</b> {i[2]}
        <b>Количество:</b> {i[3]}
        <b>Цена:</b> {i[5]}
        ------------------\n
        '''
    else:
        for j in res:
            all_comment = ''
            comment = await db.sql_user_nameProd_user_compound(message.from_user.id, j[2])

            p = 0
            for k in comment:
                count_compound = 0
                c = ''

                price_compound = comment[p][4]
                const_count_compound = comment[p][5]
                for i in price_compound:
                    if i.isdigit():
                        c += i
                        count_compound = c
                p += 1

                if k[6] != 'null':
                    all_comment += k[6] + ' '
                elif count_compound > const_count_compound:
                    all_comment += f"\n{k[3]} - {k[4]}"
            sum += float(j[5])
            text += f'''
<b>Название:</b> {j[2]}
<b>Количество:</b> {j[3]}
<b>Цена:</b> {j[5]}
<b>Коментарий:</b> {all_comment}
------===------------------\n
                            '''

    if sum == 0:
        await message.answer("Ваша корзина пуста, сделайте заказ")
    else:
        await message.answer(text=text, parse_mode="HTML")
        await message.answer(f"Общая сумма составит: {round(sum, 2)} бл.р",
                             reply_markup=await confirm_order_inline_keyboard())


@dp.callback_query_handler(lambda call: "confirm_" in call.data)
async def confirm_basket_user(message: types.Message):
    confirm = await db.sql_delete_basket_user(message.from_user.id)
    all_name_prod = await db.sql_user_nameProd_Com_user_compound(message.from_user.id)
    if all_name_prod != '':
        await db.sql_delete_user_compound(message.from_user.id)

    if not confirm:
        await message.answer("Вы потвердили заказ: ")


@dp.callback_query_handler(lambda call: "del_" in call.data)
async def confirm_basket_user(call: types.CallbackQuery):
    delete_product = await db.sql_show_basket(call.from_user.id)

    for i in delete_product:
        await call.message.answer(f'<b>Название:</b> {i[2]}',
                                  reply_markup=await delete_prod_inline_keyboard(i[2]))


@dp.callback_query_handler(lambda call: "delProd_" in call.data)
async def confirm_basket_user(call: types.CallbackQuery):
    name_product = call.data.split("_")[1]
    print(name_product)
    res = await db.sql_delete_product_basket_user(call.from_user.id, name_product)

    all_name_prod = await db.sql_user_nameProd_Com_user_compound(call.from_user.id)
    if all_name_prod != '':
        await db.sql_delete_product_user_compound(call.from_user.id, name_product)

    if not res:
        await call.answer(f'Вы успешно удалили: {name_product}', show_alert=False)
