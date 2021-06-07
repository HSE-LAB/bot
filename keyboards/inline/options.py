import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import place_order_callback


async def show_categories_buttons(categories: list):
    buttons = []
    for category in categories:
        if category == "Напитки":
            buttons.append(
                [InlineKeyboardButton(text=f'🥤 {category}', switch_inline_query_current_chat=f"{category}")])
        elif category == "Снеки":
            buttons.append(
                [InlineKeyboardButton(text=f'🍏 {category}', switch_inline_query_current_chat=f"{category}")])
        elif category == "Завтраки":
            buttons.append(
                [InlineKeyboardButton(text=f'🧇 {category}', switch_inline_query_current_chat=f"{category}")])
        else:
            buttons.append([InlineKeyboardButton(text=f'{category}', switch_inline_query_current_chat=f"{category}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def buy_item(item_name, item_price, flavour):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Купить {item_name}, 💸{item_price} ",
                              callback_data=f'buy:{item_name}:{item_price}:{flavour}')],
    ])


async def make_order():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Изменить корзину 🗑️", callback_data="change")],
        [InlineKeyboardButton(text="✅ Оформить заказ ✅", callback_data="order")],
    ])



async def process_user_info(data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"order:no:{data}"),
            InlineKeyboardButton(text="✅️", callback_data=f"order:yes:{data}")
        ],
    ])


async def delete_all_orders():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑️ Удалить все заказы️", callback_data="delete:delete")
        ],
    ])

async def change_cart_keyboard(quantity, item):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"➖", callback_data=f"change:minus:{item}"),
            InlineKeyboardButton(text=f"{quantity}", callback_data=f"order"),
            InlineKeyboardButton(text=f"➕", callback_data=f"change:plus:{item}")
        ],
        [InlineKeyboardButton(text=f"❌ Удалить ❌", callback_data=f"change:delete:{item}")],
    ])
