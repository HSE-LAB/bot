
# import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import message

from loader import dp, db

from keyboards.default.options import options


async def show_about(m: types.Message):
    txt = "Добро пожаловать в наш ЗОЖ МАРКЕТ!!!\n"\
        "Чтобы увидеть все команды воспользуйтесь командой '\help'"\
            "Чтобы начать просмотр магазина нажмите '\start'"
    await message.answer(txt)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Выберите товар из меню ниже", reply_markup=options)

