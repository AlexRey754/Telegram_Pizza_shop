import keyboards

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp,bot
from utils.db_api import db
from data.config import ADMINS,PAYMENT_TOKEN

from states import OrderState


@dp.message_handler(state=OrderState.adress)
async def reg_adress(message: types.Message, state: FSMContext):
    uid = message.from_user.id
    adress = message.text
    db.add_adress(uid,adress)
    await message.answer('Отлично!')
    await message.answer('У нас есть следующие категории продукции',reply_markup=keyboards.inline.create_order)
    await state.finish()


@dp.callback_query_handler(text='pizza',state='*')
async def show_pizzas(call:types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=keyboards.inline.create_dynamic_keyboard_for_order('Піца'))

@dp.callback_query_handler(text='drink',state='*')
async def show_drinks(call:types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=keyboards.inline.create_dynamic_keyboard_for_order('Напій'))

@dp.callback_query_handler(text='dessert',state='*')
async def show_desserts(call:types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=keyboards.inline.create_dynamic_keyboard_for_order('Десерт'))

@dp.callback_query_handler(text='back_to_menu',state='*')
async def back_menu(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=keyboards.inline.create_order)

@dp.callback_query_handler(text_contains='buy',state='*')
async def buy_item(call: types.CallbackQuery):
    item_id = int(call.data[4:])
    user_id = call.from_user.id
    db._add_to_cart(user_id,item_id)
    await call.answer(f'Добавлено!')

@dp.callback_query_handler(text='cart',state='*')
async def get_cart(call: types.CallbackQuery,state: FSMContext):
    uid = call.from_user.id
    
    data = db._list_order(uid)
    user_adress = db.get_adress(uid)

    if data:
        text = ''
        sum = 0
        for _, products in data:
            sum += products.price
            text = text + f'''{products.name} - {products.price} грн.\n'''
        text += f'\nАдрес: {user_adress}'
        text += f'\n\n Итого: {sum} грн.'
        await call.message.answer(text,reply_markup=keyboards.inline.purchase)
    else:
        await call.answer('Вы еще ничего не выбрали')

@dp.callback_query_handler(text='purchase',state='*')
async def make_purchase(call: types.CallbackQuery,state: FSMContext):


    await call.message.edit_reply_markup(reply_markup=None)
    uid = call.from_user.id

    data = db._list_order(uid)
    prices = [types.LabeledPrice(label=i.name, amount=i.price*100) for _,i in data]

    await bot.send_invoice(uid,
                           title='Заказ',
                           description='Вкусно и быстро',
                           provider_token=PAYMENT_TOKEN,
                           currency='UAH',
                           need_email=False,
                           prices=prices,
                           start_parameter='example',
                           payload='some_invoice')
    
@dp.callback_query_handler(text='cancel')
async def make_purchase(call: types.CallbackQuery):
    uid = call.from_user.id
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.edit_text('Покупки сброшены')
    await call.message.answer('Меню',reply_markup=keyboards.default.menu)
    db.delete_cart(uid)

# Хендлер подтверждения оплаты
@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def s_pay(message: types.Message):
    # Отправка пользователю подтверждения об оплате
    uid = message.from_user.id
    await bot.send_message(message.chat.id, 'Платеж прошел успешно!!!',reply_markup=keyboards.default.menu)


    # Генерация сообщения админам бота
    data = db._list_order(uid)
    user_adress = db.get_adress(uid)
    text = '<b>НОВЫЙ ЗАКАЗ</b>\n\n'
    for _, products in data:
        text = text + f'''{products.name}.\n'''
    text += f'\n<b>Адрес</b>: {user_adress}'
    
    # отправка админам бота сообщения с заказом
    for admin_uid in ADMINS:
        await bot.send_message(admin_uid,text)

    # Очистка корзины
    db.delete_cart(message.from_user.id)
