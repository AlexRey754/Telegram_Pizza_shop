from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from data.config import ADMINS
from states import AddPosition
from utils.db_api import db
import keyboards

@dp.message_handler(state=AddPosition.name)
async def reg_pos_name(message: types.Message, state: FSMContext):
    temp = message.text
    if temp == '❌Отмена':
        await state.finish()
        await message.answer('Отмена',reply_markup=keyboards.default.menu)
    else:
        await state.update_data(name=temp)
        await message.answer('Введите описание')
        await AddPosition.description.set()

@dp.message_handler(state=AddPosition.description)
async def reg_pos_description(message: types.Message, state: FSMContext):
    temp = message.text
    if temp == '❌Отмена':
        await state.finish()
        await message.answer('Отмена',reply_markup=keyboards.default.menu)
    else:
        await state.update_data(description=temp)
        await message.answer('Введите цену')
        await AddPosition.price.set()

@dp.message_handler(state=AddPosition.price)
async def reg_pos_price(message: types.Message, state: FSMContext):
    
    if message.text == '❌Отмена':
        await state.finish()
        await message.answer('Отмена',reply_markup=keyboards.default.menu)
    else:
        data = await state.get_data()

        name = data.get('name')
        description = data.get('description')
        price = int(message.text) * 100   # Особенность платежной системы Телеграмм

        db.add_position_to_db(name, description, price)

        await message.answer('Готово',reply_markup=keyboards.default.admin_menu)
        await state.finish()
