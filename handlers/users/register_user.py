from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from states import Register
from utils.db_api import db
import keyboards

@dp.message_handler(state=Register.name)
async def reg_name(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(name=text)
    await message.answer('Введите контактный номер телефона')
    await Register.tel_number.set()

@dp.message_handler(state=Register.tel_number)
async def reg_number(message: types.Message, state: FSMContext):

    tel_number = message.text

    if tel_number.startswith('+380') and len(tel_number)==13:

        data = await state.get_data()
        uid = message.from_user.id
        name = data.get('name')
        
        db.register_user(uid, name, tel_number)
        await message.answer('Регистрация успешно завершена. Для оформления заказа нажмите кнопку "Сделать заказ"',reply_markup=keyboards.default.menu)
        await state.finish()
    else:
        await message.answer('Введите корректный номер телефона.Пример: +380ХХХХХХХХХ')
