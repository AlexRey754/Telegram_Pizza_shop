from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db import _show_pos_list, _show_list_category,get_item

buy = CallbackData('buy','item_id')
item = CallbackData('item','item_id')
category = CallbackData('category','category_name')

purchase = InlineKeyboardMarkup(row_width=1)
purchase.add(
    InlineKeyboardButton('Добавить Адрес доставки',callback_data='add_adress'),
    InlineKeyboardButton('Сбросить',callback_data='cancel'),
    InlineKeyboardButton('Назад',callback_data='back_to_menu'),


)

purchase_complete = InlineKeyboardMarkup(row_width=1)
purchase_complete.add(
    InlineKeyboardButton('Перейти к оплате',callback_data='purchase'),
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

    for product in _list:
        buttons_list.append([InlineKeyboardButton(text=f'{product.name}', callback_data=item.new(item_id=product.id))])

    buttons_list.append([InlineKeyboardButton(text='Назад',callback_data='back_to_menu')])
    keyboard_inline_buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)
    return keyboard_inline_buttons

def confirm_product(id):

    keyboard_inline_buttons = InlineKeyboardMarkup(row_width=1)
    keyboard_inline_buttons.insert(
            InlineKeyboardButton(text='Добавить в корзину', callback_data=buy.new(item_id=id))
            )
    keyboard_inline_buttons.insert(InlineKeyboardButton(text='Назад',callback_data='back_to_menu_from_product'))
    return keyboard_inline_buttons