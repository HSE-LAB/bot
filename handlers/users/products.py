import logging
from loader import dp, db
from aiogram.types import  CallbackQuery, message,InlineQuery,InlineQueryResultPhoto,InputTextMessageContent,InlineQueryResultArticle
from keyboards.inline.options import buy_item
from keyboards.default.options import options
@dp.inline_handler()
async def empty_query(query: InlineQuery):
    items = [ dict(name=item['name'],price=item['price'],id=item['id'],img_link=item['img_link']) for item in await db.select_products_from_category(category=query.query)]
    logging.info(items)
    articles = [
        InlineQueryResultPhoto(
        id=f'{item["id"]}',
        title=item['name'],
        thumb_url=item['img_link'],
        photo_url=item['img_link'],
        description=item['name'],
        caption=f"{item['name']}, Стоит: 🤑 {item['price']}",
        reply_markup=await buy_item(item['name'])) 
        for item in items
        ]
    await query.answer(articles)
    
# @dp.callback_query_handler(text_contains="category")
# async def select_category(call: CallbackQuery):
#     call.answer()
#     callback_data = call.data
#     category = callback_data[callback_data.find(":")+1:]
#     items = [ dict(name=item['name'],price=item['price']) for item in await db.select_products_from_category(category=category)]
#     await call.message.answer(items)
    