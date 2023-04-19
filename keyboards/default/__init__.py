from aiogram.types import ReplyKeyboardMarkup,KeyboardButton



menu = ReplyKeyboardMarkup(True,True)
menu.row(KeyboardButton('➕Сделать заказ'))
# menu.row(KeyboardButton('🛒Корзина'))


settings = ReplyKeyboardMarkup(True,True)
settings.row(KeyboardButton('📋Список всех позиций по группам'))
settings.row(KeyboardButton('👨‍🦳 Список пользователей'))
settings.row(KeyboardButton('✍️Изменить цену на позицию'))
settings.row(KeyboardButton('◀️Главное меню'))


cancel = ReplyKeyboardMarkup(True, True)
cancel.row(KeyboardButton('❌Отмена'))
