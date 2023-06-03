import keyboards

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from utils.db_api import db
from data.config import ADMINS,PAYMENT_TOKEN
from states import OrderState
from loader import bot


@dp.message_handler(content_types=['text'])
async def text_buttons_func(message: types.Message, state: FSMContext):
    if message.text.startswith('/del'):
        uid = message.from_user.id
        item_id = message.text[4:]
        db.delete_product_from_cart(item_id,uid) 
        cart = db.generate_user_cart(uid)

        if cart:
            await message.answer(cart,reply_markup=keyboards.inline.purchase)
        else:
            await message.answer('Корзина пуста')

    elif message.text.startswith('/see_'):
        try:
            raw_date = message.text[5:]
            date = raw_date.replace('_','-')
            text = db.generate_orders_list(date,raw_date)
            await message.answer(text)
        except:
            await message.answer('Нет записей по этому дню')

    elif message.text.startswith('/order'):
        raw_data = message.text[7:]
        date = raw_data[:10].replace('_','-')
        time = raw_data[11::].replace('_',':')
        text = db.generate_current_order(date, time)
        await message.answer(text)

    match message.text:
        case '➕Сделать заказ':
            await message.answer('Обратите внимание!', reply_markup=types.ReplyKeyboardRemove())
            await message.answer('У нас есть следующие категории продукции',reply_markup=keyboards.inline.categories_keyboard())

        case '📋Список заказов':
            try:
                text = db.generate_dates_list()
                await message.answer(text)
            except:
                await message.answer('Пока нет позиций в базе')

        case '👨‍🦳 Список пользователей':
            text = db.generate_user_list()
            await message.answer(text)

        case '◀️Главное меню': 
                await message.answer('Меню',reply_markup=keyboards.default.menu)

