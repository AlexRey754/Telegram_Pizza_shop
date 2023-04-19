from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from states import ChangePrice
from utils.db_api import db
import keyboards

@dp.message_handler(state=ChangePrice.id)
async def reg_id(message: types.Message, state: FSMContext):

    if message.text == '❌Отмена':
        await state.finish()
        await message.answer('Изменения отменены!',reply_markup=keyboards.default.menu)
    else:
        try:
            raw_text = int(message.text)
            await state.update_data(id=raw_text)
            await message.answer('Введите новую цену',reply_markup=keyboards.default.cancel)
            await ChangePrice.price.set()
        except:
            await message.answer('Введите число')

@dp.message_handler(state=ChangePrice.price)
async def reg_new_price(message: types.Message, state: FSMContext):
    if message.text == '❌Отмена':
        await state.finish()
        await message.answer('Изменения отменены!',reply_markup=keyboards.default.menu)
    else:
        price = int(message.text)

        data = await state.get_data()
        id = int(data.get('id'))
        
        db.change_price(id,price)

        await message.answer('Цена успешно изменена',reply_markup=keyboards.default.settings)
        await state.finish()

