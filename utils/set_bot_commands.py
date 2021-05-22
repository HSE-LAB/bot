from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("help", "Показать все команды"),
        types.BotCommand("about", "О нас")
        ])
        