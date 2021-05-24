import logging

import asyncpg

from loader import dp, db
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.inline.options import show_categories_buttons, make_order


@dp.message_handler(Text(equals="🔍 Каталог"))
async def show_categories(message: Message):
    categories = [category['category'] for category in await db.select_all_categories()]
    await message.answer("В нашем магазине продаются товары следующих категорий",
                         reply_markup=await show_categories_buttons(categories))


@dp.message_handler(Text(equals="🧮 Мои заказы"))
async def show_orders(message: Message):
    orders = [
        dict(date=item['date'], quantity=item['quantity'], product_id=item['product_id'],
             sum=item['sum'], buyer=item['buyer'])
        for item in await db.select_user_orders(telegram_id=message.from_user.id)]

    if not orders:
        await message.answer(text="Ты еще не заказывал наши полезнейшие продукты 😱\n\n"
                                  "Нажми на '🔍 Каталог' в нижней панели, чтобы посмотреть наши товары😉")
        return

    count = 1
    order = 'Покупки:\n'
    for item in orders:
        date = item.get("date")
        quantity = item.get("quantity")
        product_id = int(item.get("product_id"))
        ord_sum = item.get("sum")
        buyer = item.get("buyer")

        buyer_name = [dict(name=item['fio']) for item in await db.select_user_name_by_tg_id(buyer)]
        buyer_name = buyer_name[0].get("name")

        product = [dict(name=item['name']) for item in await db.select_product_by_id(product_id)]
        product = product[0].get("name")
        product_flover = [dict(flavour=item['flavour']) for item in await db.select_product_flavour_by_id(product_id)]
        product_flover = product_flover[0].get("flavour")

        order += f'USER: {buyer_name}\n' \
                 f'{count}. 📅: {date} | 🛒: {product} | 💣: {product_flover} | 🛍️: {quantity} | 💰:{ord_sum}\n'
        count += 1
    await message.answer(text=order)


@dp.message_handler(Text(equals="🛒 Моя корзина"))
async def show_cart(message: Message, state: FSMContext):
    item_string = "\n"
    total = 0
    cart = (await state.get_data()).get("cart")
    if (cart is None) or (not len(cart)):
        await message.answer(text="😞Ваша корзина пуста😞\n\n" \
                                  "Нажми на '🔍 Каталог' в нижней панели, чтобы посмотреть наши товары😉")
        return
    for item in cart:
        total += int(cart[item]['price']) * int(cart[item]['quantity'])
        item_string = "".join([item_string, f"{item}: ",
                               f"{cart[item]['price']} * {cart[item]['quantity']}\n" \
                               f"😋Вкус: {cart[item]['flavour']}😋\n" \
                               f"💵На сумму: {int(cart[item]['price']) * int(cart[item]['quantity'])}💵\n\n"])
    txt = f'✨✨✨✨✨✨\n' \
          "В вашей корзине находятся следующие товары:\n" \
          f"{item_string}\n" \
          f"Общая сумма заказа: 💲{total}\n" \
          "✨✨✨✨✨✨\n"
    await message.answer(text=txt, reply_markup=await make_order())
