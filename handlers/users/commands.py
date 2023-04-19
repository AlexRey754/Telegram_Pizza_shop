import keyboards

from data.config import ADMINS

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.db_api import db
from states import Register

@dp.message_handler(Command('start'))
async def bot_start(message: types.Message):

    uid = message.from_user.id
    is_register = db.check_user_registration(uid)
    if is_register == False:
        await message.answer(f'Здравствуйте! Прежде чем начать использовать функции данного бота пройдите пожалуйта небольшую регистрацию!\n\nВведите ФИО!')
        await Register.name.set()
    else:
        await message.answer(f'С возвращением!',reply_markup=keyboards.default.menu)


@dp.message_handler(Command('admin'))
async def admin_check(message: types.Message):

    uid = str(message.from_user.id)
    if uid in ADMINS:
        await message.answer('Ваш ID был зарегестрирован с правами администратора',reply_markup=keyboards.default.settings)
    else:
        await message.answer('У вас недостаточно прав для использования данной команды')


@dp.message_handler(Command('help'))
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку"
            )
    
    await message.answer("\n".join(text))
