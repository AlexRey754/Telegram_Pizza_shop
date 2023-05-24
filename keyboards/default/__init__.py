from aiogram.types import ReplyKeyboardMarkup,KeyboardButton



menu = ReplyKeyboardMarkup(True,True)
menu.row(KeyboardButton('➕Сделать заказ'))

settings = ReplyKeyboardMarkup(True,True)
settings.row(KeyboardButton('📋Список заказов'))
settings.row(KeyboardButton('👨‍🦳 Список пользователей'))
settings.row(KeyboardButton('◀️Главное меню'))


cancel = ReplyKeyboardMarkup(True, True)
cancel.row(KeyboardButton('❌Отмена'))
