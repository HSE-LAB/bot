import logging
from loader import dp,db
from aiogram.types import Message, CallbackQuery

from aiogram.dispatcher.filters import Text
from keyboards.inline.options import show_categories_buttons


@dp.message_handler(Text(equals="🔍 Каталог"))
async def show_categories(message: Message):
    categories = [category['category'] for category in await db.select_all_categories()]
    await message.answer("В нашем магазине продаются товары следующих категорий", reply_markup=await show_categories_buttons(categories))