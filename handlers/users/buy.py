
from aiogram.types import CallbackQuery
from loader import dp,bot
import logging

from keyboards.inline.callback_datas import buy_callback
from aiogram.dispatcher import FSMContext

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@dp.callback_query_handler(buy_callback.filter())
async def purchase_item(call:CallbackQuery,state,callback_data:dict):
    price = callback_data.get("price")
    item = callback_data.get("item")
    cart = (await state.get_data()).get("cart")
    if item in cart:
        async with state.proxy() as data:
           data["cart"][item]['quantity'] +=1
    else:
        async with state.proxy() as data:
            data["cart"][item] = {"price" : price,'quantity':1 }
    cart = (await state.get_data()).get("cart")
    await bot.edit_message_reply_markup(
  inline_message_id = call.inline_message_id, reply_markup =  InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Купить {item}, 💸{price} ({cart[item]['quantity']})",callback_data=f'buy:{item}:{price}')],
    ]))

