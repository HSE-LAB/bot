import logging
from loader import dp, bot
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.inline.options import change_cart_keyboard
from keyboards.inline.callback_datas import change_callback


@dp.callback_query_handler(text="change")
async def change_cart(call: CallbackQuery, state: FSMContext):
    cart = (await state.get_data()).get("cart")
    for item in cart:
        flavour = cart[item]['flavour']
        if item == "Мюсли":
            await call.message.answer(text=f"🥣 Мюсли🥣\n😋Вкус:{flavour}😋",
                                      reply_markup=await change_cart_keyboard(cart[item]['quantity'], item))
        elif item == "Протеиновый коктель":
            await call.message.answer(text=f"🥤 Коктель🥤\n😋Вкус:{flavour}😋",
                                      reply_markup=await change_cart_keyboard(cart[item]['quantity'], item))
        elif item == "Протеиновый батончик":
            await call.message.answer(text=f"🍫 Батончик 🍫\n😋Вкус:{flavour}😋",
                                      reply_markup=await change_cart_keyboard(cart[item]['quantity'], item))
        elif item == "Пастила":
            await call.message.answer(text=f"〰️ Пастила 〰️\n😋Вкус:{flavour}😋",
                                      reply_markup=await change_cart_keyboard(cart[item]['quantity'], item))


@dp.callback_query_handler(change_callback.filter(action="minus"))
async def minus_item(call: CallbackQuery, state: FSMContext, callback_data: dict):
    item = callback_data.get("item")
    cart = (await state.get_data()).get("cart")
    # logging.info(cart[item]['quantity'])
    if cart[item]['quantity'] == 1:
        # logging.info(cart[item]['quantity'],"ddd")
        await call.answer(text="Нельзя больше уменьшить", show_alert=True)
    else:
        async with state.proxy() as data:
            data["cart"][item]['quantity'] -= 1
        await bot.edit_message_reply_markup(
            message_id=call.message.message_id, chat_id=call.message.chat.id,
            reply_markup=await change_cart_keyboard((await state.get_data()).get("cart")[item]['quantity'], item))


@dp.callback_query_handler(change_callback.filter(action="plus"))
async def minus_item(call: CallbackQuery, state: FSMContext, callback_data: dict):
    item = callback_data.get("item")
    async with state.proxy() as data:
        data["cart"][item]['quantity'] += 1
    await bot.edit_message_reply_markup(
        message_id=call.message.message_id, chat_id=call.message.chat.id,
        reply_markup=await change_cart_keyboard((await state.get_data()).get("cart")[item]['quantity'], item))


@dp.callback_query_handler(change_callback.filter(action="delete"))
async def delete_item(call: CallbackQuery, state: FSMContext, callback_data: dict):
    item = callback_data.get("item")
    async with state.proxy() as data:
        data["cart"].pop(item, None)
    await bot.edit_message_text(
        message_id=call.message.message_id, chat_id=call.message.chat.id, text=f"{item} удалено", reply_markup=None)
