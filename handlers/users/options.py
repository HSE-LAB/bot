import logging
from loader import dp,db
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.inline.options import show_categories_buttons,make_order


@dp.message_handler(Text(equals="🔍 Каталог"))
async def show_categories(message: Message):
    categories = [category['category'] for category in await db.select_all_categories()]
    await message.answer("В нашем магазине продаются товары следующих категорий", reply_markup=await show_categories_buttons(categories))

@dp.message_handler(Text(equals="🛒 Моя корзина"))
async def show_cart(message: Message, state: FSMContext):
    item_string = "\n"
    total = 0
    cart = (await state.get_data()).get("cart")
    if not len(cart):
        await message.answer(text="😞Ваша корзина пуста😞\n\n"\
         "Нажми на '🔍 Каталог' в нижней панели, чтобы посмотреть наши товары😉")
        return
    for item in cart:
        total += int(cart[item]['price']) * int(cart[item]['quantity'])
        item_string = "".join([item_string,f"{item}: ",
                        f"{cart[item]['price']} * {cart[item]['quantity']}\n"\
                        f"💵На сумму: {int(cart[item]['price']) * int(cart[item]['quantity'])}💵\n"])
    txt = f'✨✨✨✨✨✨\n'\
         "В вашей корзине находятся следующие товары:\n"\
         f"{item_string}\n"\
         f"Общая сумма заказа: 💲{total}\n"\
         "✨✨✨✨✨✨\n"
    await message.answer(text=txt,reply_markup=await make_order())
    





