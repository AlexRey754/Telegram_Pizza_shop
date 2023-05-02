from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db import _show_pos_list, _show_list_category

buy = CallbackData('buy','item_id')
category = CallbackData('category','category_name')


purchase = InlineKeyboardMarkup(row_width=1)
purchase.add(
    InlineKeyboardButton('Подтвердить',callback_data='purchase'),
    InlineKeyboardButton('Сбросить',callback_data='cancel')

)


def categories_keyboard():
    _list = _show_list_category()
    keyboard_inline_buttons = InlineKeyboardMarkup()

    for item in _list:
        keyboard_inline_buttons.insert(
            InlineKeyboardButton(text=f'{item.category}', callback_data=category.new(category_name=item.category))
            )
    keyboard_inline_buttons.add(InlineKeyboardButton('Корзина',callback_data='cart'))
    keyboard_inline_buttons.add(InlineKeyboardButton('❌Отменить заказ',callback_data='cancel'))

    return keyboard_inline_buttons

def products_from_category(name):

    _list = _show_pos_list(name)
    buttons_list = []

    for item in _list:
        buttons_list.append([InlineKeyboardButton(text=f'"{item.name}" {item.price} грн.', callback_data=buy.new(item_id=item.id))])

    buttons_list.append([InlineKeyboardButton(text='Назад',callback_data='back_to_menu')])
    keyboard_inline_buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    return keyboard_inline_buttons
