
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

options = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧮 Мои заказы"),
        ],
        [
            KeyboardButton(text="🔍 Каталог"),
            KeyboardButton(text="🛒 Моя корзина")
        ],
    ],
    resize_keyboard=True,

)