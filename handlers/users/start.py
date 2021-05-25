import logging
from aiogram.dispatcher import FSMContext
# import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import message
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile

from loader import dp,bot

from keyboards.default.options import options

from states.state import UserStatus

async def show_about(m: types.Message):
    txt = "Добро пожаловать в наш ЗОЖ МАРКЕТ!!!\n"\
        "Чтобы увидеть все команды воспользуйтесь командой '\help'"\
        "Чтобы начать просмотр магазина нажмите '\start'"
    await message.answer(txt)


@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message, state: FSMContext):
    if not (await state.get_data()).get("cart"):
        await state.update_data({"cart": {}})
    await message.answer("Добро пожаловать в наш ЗОЖ МАРКЕТ!!!", reply_markup=options)

@dp.message_handler(Command("about"))
async def bot_start(message: types.Message):
    txt = "Данный проект был разработан специально для лабы по базам данных\n"\
        "Спасибо, что протестировали наш проект, надеемся, он вам понравился❤️"
    photo = InputFile(path_or_bytesio="photos/cat.jpg")  # Local file
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=photo,
                         caption=txt)
    