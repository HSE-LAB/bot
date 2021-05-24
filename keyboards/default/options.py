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
    resize_keyboard=True)

phone = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text="☎️Отправить",
                           request_contact=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True)


location = ReplyKeyboardMarkup(keyboard=[

    [
        KeyboardButton(text="📍 Отправить",
                       request_location=True)
    ]
],
    resize_keyboard=True,
    one_time_keyboard=True)

done = ReplyKeyboardMarkup(keyboard=[

    [
        KeyboardButton(text='🔥 DONE 🔥 ')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=True)
