from aiogram import executor
import logging
from loader import dp,db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    logging.info("Создаем подключение к базе данных")
    await db.create()

    # await db.drop_users()

    logging.info("Создаем таблицу пользователей")
    await db.create_table_users()
    logging.info("Готово.")
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
