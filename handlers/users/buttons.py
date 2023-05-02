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

        case _:
            await message.answer('Неизвестная команда')

