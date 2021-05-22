import logging
from aiogram.dispatcher import FSMContext
# import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import message

from loader import dp, db

from keyboards.default.options import options

from states.state import UserStatus

async def show_about(m: types.Message):
    txt = "Добро пожаловать в наш ЗОЖ МАРКЕТ!!!\n"\
        "Чтобы увидеть все команды воспользуйтесь командой '\help'"\
        "Чтобы начать просмотр магазина нажмите '\start'"
    await message.answer(txt)


@dp.message_handler(CommandStart(),state=None)
async def bot_start(message: types.Message,state: FSMContext):
    await state.update_data(
        {"cart": {}}
    )
    # await UserStatus.user_cart.set()
    await message.answer("Добро пожаловать в наш ЗОЖ МАРКЕТ!!!", reply_markup=options)

