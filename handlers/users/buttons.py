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
        db.delete_product_from_order(item_id,uid)
           
        data = db._list_order(uid)
        user = db.get_user(uid)
        # await message.delete()


        if data:
            text = ''
            sum = 0
            for _, products in data:
                item_count = db.get_count_in_order(uid,products.id)
                sum += products.price * item_count
                text = text + f'''{products.name} (<b>x{item_count}</b>) - {products.price} грн | /del{products.id}\n'''
            text += f'\nАдрес: {user.adress}'
            text += f'\n\n Итого: {sum} грн.'
            await message.answer(text,reply_markup=keyboards.inline.purchase)

        else:
            await message.answer('Корзина пуста')

    match message.text:
        case '➕Сделать заказ':
            await state.finish()
            await message.answer('Введите адрес доставки в формате [город][улица][дом\квартира]',reply_markup=types.ReplyKeyboardRemove())
            await OrderState.adress.set()

        case '📋Список всех позиций по группам':
            try:
                row_text = db.show_all_position()
                await message.answer(row_text)
            except:
                await message.answer('Пока нет позиций в базе')

        case '👨‍🦳 Список пользователей':
            text = db.show_all_users()
            await message.answer(text)

        case '◀️Главное меню': 
                await message.answer('Меню',reply_markup=keyboards.default.menu)

