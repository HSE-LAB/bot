import logging

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

async def on_startup(dispatcher):
    # Уведомляет про запуск
    logging.info("Создаем подключение к базе данных")
    await db.create()
    

    # await db.drop_products()

    logging.info("Создаем таблицу пользователей")
    await db.create_table_users()
    await db.create_table_orders()
    await db.create_table_products()
    logging.info("Готово.")

    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
