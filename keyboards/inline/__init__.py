from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db import _show_pos_list

buy = CallbackData('buy','item_id')

create_order = InlineKeyboardMarkup()
create_order.add(
    InlineKeyboardButton('Піца',callback_data='pizza'),
    InlineKeyboardButton('Напої',callback_data='drink'),
    InlineKeyboardButton('Десерти',callback_data='dessert'),

)
create_order.add(
    InlineKeyboardButton('Корзина',callback_data='cart'),
)
create_order.add(
    InlineKeyboardButton('❌Отменить заказ',callback_data='cancel'),
)

purchase = InlineKeyboardMarkup(row_width=1)
purchase.add(
    InlineKeyboardButton('Подтвердить',callback_data='purchase'),
    InlineKeyboardButton('Сбросить',callback_data='cancel')

)


def create_dynamic_keyboard_for_order(name):

    _list = _show_pos_list(name)
    buttons_list = []

    for item in _list:
        buttons_list.append([InlineKeyboardButton(text=f'"{item.name}" {item.price} грн.', callback_data=buy.new(item_id=item.id))])

    buttons_list.append([InlineKeyboardButton(text='Назад',callback_data='back_to_menu')])
    keyboard_inline_buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    return keyboard_inline_buttons
