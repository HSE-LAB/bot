import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import category_callback

async def show_categories_buttons(categories: list):
    buttons = []
    for category in categories:
        if (category == "Напитки"):
            buttons.append([InlineKeyboardButton(text=f'🥤 {category}', switch_inline_query_current_chat=f"{category}")])
        elif (category == "Снеки"):
            buttons.append([InlineKeyboardButton(text=f'🍏 {category}', switch_inline_query_current_chat=f"{category}")])
        elif (category == "Завтраки"):
            buttons.append([InlineKeyboardButton(text=f'🧇 {category}', switch_inline_query_current_chat=f"{category}")])
        else:
            buttons.append([InlineKeyboardButton(text=f'{category}', switch_inline_query_current_chat=f"{category}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def buy_item(item_name):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Купить {item_name}",callback_data='buy')],
    ])