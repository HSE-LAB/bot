from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData("buy", "item", 'price', "flavour")

change_callback = CallbackData("change", "action", "item")

order_callback = CallbackData("order", "change", "data")

place_order_callback = CallbackData("order", "mode")

delete_order_callback = CallbackData("delete", "delete")
