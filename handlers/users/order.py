from asyncio import sleep

import asyncpg
import requests
from aiogram import types
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.options import options, phone, location, done
from keyboards.inline.options import change_cart_keyboard, process_user_info
from loader import dp, bot, db
import logging

from keyboards.inline.callback_datas import order_callback, place_order_callback
from aiogram.dispatcher import FSMContext

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states import UserName


@dp.callback_query_handler(text="order")
async def make_order(call: CallbackQuery):
    user_name = call.from_user.full_name
    msg_name = f'Вас зовут: {user_name}'
    data = 'name'
    await call.message.answer(text=msg_name,
                              reply_markup=await process_user_info(data))


@dp.callback_query_handler(order_callback.filter(change="no", data='name'))
async def change_name(call: CallbackQuery):
    await call.message.answer(text="😉 Введите свое имя")
    await UserName.changed_name.set()


@dp.message_handler(state=UserName.changed_name)
async def changed_name(msg: types.Message, state: FSMContext):
    new_name = msg.text
    await state.update_data(name=new_name)

    try:
        user = await db.select_user(telegram_id=msg.from_user.id)
        await db.update_user_name(telegram_id=msg.from_user.id, new_fio=new_name)
    except asyncpg.exceptions.ExclusionViolationError:
        pass

    await msg.answer(f"❗ Ваше имя изменено: {new_name}")

    await msg.answer(text="Нажмите '☎️Отправить, чтобы прислать нам свой номер телефона.",
                     reply_markup=phone)

    await UserName.num_settings.set()


@dp.callback_query_handler(order_callback.filter(change="yes",
                                                 data='name'))
async def accept_name(call: CallbackQuery, state: FSMContext):
    user_name = call.from_user.full_name
    await state.update_data(name=user_name)

    try:
        user = await db.select_user(telegram_id=call.from_user.id)
        await db.update_user_name(telegram_id=call.from_user.id, new_fio=user_name)
    except asyncpg.exceptions.ExclusionViolationError:
        pass

    await call.message.answer(text="Нажмите '☎️Отправить, чтобы прислать нам свой номер телефона.",
                              reply_markup=phone)
    await UserName.num_settings.set()


@dp.message_handler(state=UserName.num_settings,
                    content_types=types.ContentTypes.CONTACT)
async def set_num_settings(message: types.Message, state: FSMContext):
    # await message.answer('Идем дальше 😀', reply_markup=ReplyKeyboardRemove())  # del keyboard
    user_telephone_num = message.contact.phone_number
    await state.update_data(num=user_telephone_num)

    await message.answer(text="Нажмите '📍 ️Отправить, чтобы прислать нам свою локацию.",
                         reply_markup=location)
    await UserName.addr_settings.set()


def get_address_from_coords(coords):
    PARAMS = {
        # "apikey": "e280e529-4b28-4b3d-a6d0-4b69d326cbca",  # hse bot
        "apikey": "85b875fe-e1e7-4bf3-a513-db593670e686",  # orig bot
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str

    except Exception as e:
        return None


@dp.message_handler(state=UserName.addr_settings,
                    content_types=types.ContentTypes.LOCATION)
async def set_addr_settings(message: types.Message, state: FSMContext):
    await message.answer('Обрабатываю ваш адрес... 😀', reply_markup=ReplyKeyboardRemove())  # del keyboard
    user_addr = message.location
    address_str = get_address_from_coords(user_addr)
    if address_str is None:
        msg = "Не могу определить адрес по этой локации.\n\n" \
              "Напиши, пожалуйста, адрес доставки:"
        await message.answer(text=msg,
                             reply_markup=options)
        await UserName.address.set()


    else:
        msg_num = f"Доставим по этому адресу: {address_str}"
        await state.update_data(addr=address_str)
        await message.answer(text=msg_num)


@dp.message_handler(state=UserName.address)
async def set_addr(msg: types.Message, state: FSMContext):
    new_addr = msg.text
    await state.update_data(addr=new_addr)

    await msg.answer(text="Скорей нажимай '🔥 DONE 🔥 '",
                     reply_markup=done)
    await UserName.fillin_db.set()


@dp.message_handler(state=UserName.fillin_db)
async def place_new(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = msg.from_user.id
    name = data.get('name')
    addr = data.get('addr')
    num = data.get('num')

    try:
        await db.add_user(telegram_id=telegram_id, fio=name, address=addr, phone=num)
    except asyncpg.exceptions.UniqueViolationError:
        pass

    cart = (await state.get_data()).get("cart")
    for item in cart:
        date = str(msg.date)
        prod_name = item
        quantity = cart[item]['quantity']
        flavour = cart[item]['flavour']
        total_sum = int(cart[item]['price']) * int(cart[item]['quantity'])

        product_id = [dict(id=item['id']) for item in await db.select_product_by_name_flavour(prod_name, flavour)]
        product_id = product_id[0].get("id")
        await db.add_order(date=date, quantity=quantity, product_id=product_id, sum=total_sum, buyer=telegram_id)

    await msg.answer("✨ Done", reply_markup=ReplyKeyboardRemove())  # del keyboard
    await state.finish()
    await state.update_data(
        {"cart": {}}
    )
    await msg.answer("Проверь '🧮 Мои заказы'", reply_markup=options)
