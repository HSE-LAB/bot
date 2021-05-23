import logging
from loader import dp, db

from aiogram.types import  InlineQueryResultDocument, InputFile,InlineQueryResultCachedDocument,InlineQuery,InlineQueryResultPhoto,InputTextMessageContent,InlineQueryResultArticle
from keyboards.inline.options import buy_item
from keyboards.default.options import options
from aiogram.dispatcher import FSMContext


@dp.inline_handler()
async def empty_query(query: InlineQuery,state: FSMContext):
    items = [ dict(name=item['name'],price=item['price'],id=item['id'],img_link=item['img_link']) for item in await db.select_products_from_category(category=query.query)]
    cart = (await state.get_data()).get('cart')
    
    articles = [
        InlineQueryResultArticle(
        id=f'{item["id"]}',
        title=item['name'],
        hide_url=False,
        input_message_content=InputTextMessageContent(
                    message_text=f"<b>{item['name']}</b>\n{item['img_link']}",
            parse_mode="HTML"
                ),
        url=item['img_link'],
        thumb_url=item['img_link'],
        description=f"{item['name']}, Стоит: 🤑 {item['price']}",
        reply_markup=await buy_item(item['name'],item['price'])) 
        for item in items
        ]
    await query.answer(articles)
    

    