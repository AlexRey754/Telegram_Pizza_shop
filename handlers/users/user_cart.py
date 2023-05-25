import keyboards

from aiogram import types
from aiogram.dispatcher import FSMContext, filters

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
    await message.answer('У нас есть следующие категории продукции',reply_markup=keyboards.inline.categories_keyboard())
    await state.finish()

@dp.callback_query_handler(text_contains='category',state='*')
async def show_products_for_category(call:types.CallbackQuery):
    name = call.data[9:]
    await call.message.edit_text('Выберите продукт',reply_markup=keyboards.inline.products_from_category(name))

@dp.callback_query_handler(text='back_to_menu',state='*')
async def back_menu(call: types.CallbackQuery):
    await call.message.edit_text('Выберите категорию',reply_markup=keyboards.inline.categories_keyboard())

@dp.callback_query_handler(text='back_to_menu_from_product',state='*')
async def back_menu(call: types.CallbackQuery):
    # т.к нельзя редактировать сообщение с отправленой картинкой
    await call.message.delete()
    await call.message.answer('Выберите категорию',reply_markup=keyboards.inline.categories_keyboard())

@dp.callback_query_handler(text_contains='item',state='*')
async def show_item(call: types.CallbackQuery):
    item_id = int(call.data[5:])
    item = db.get_item(item_id)
    img_path = f'./data/image/{item.img_name}'

    text = f'''
    <b> {item.name}</b>
    {item.description}

    Цена: <b>{item.price}</b>
    '''
    await call.message.delete()
    try:
        photo = open(img_path,'rb')
        await call.message.answer_photo(photo=photo, caption=text,reply_markup=keyboards.inline.confirm_product(item.id))
    except:
        await call.message.answer(text=text,reply_markup=keyboards.inline.confirm_product(item.id))
    
@dp.callback_query_handler(text_contains='buy',state='*')
async def buy_item(call: types.CallbackQuery):
    item_id = int(call.data[4:])
    user_id = call.from_user.id
    db._add_to_cart(user_id,item_id)
    await call.answer(f'Добавлено!')

@dp.callback_query_handler(text='cart',state='*')
async def get_cart(call: types.CallbackQuery,state: FSMContext):
    uid = call.from_user.id
    cart = db.generate_user_cart(uid)

    if cart:
        await call.message.edit_text(cart,reply_markup=keyboards.inline.purchase)
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
    
@dp.callback_query_handler(text='cancel',state='*')
async def cancel_purchase(call: types.CallbackQuery,state: FSMContext):
    uid = call.from_user.id
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.edit_text('Покупки сброшены')
    await call.message.answer('Меню',reply_markup=keyboards.default.menu)
    await state.finish()
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
    order = db.generate_order_to_admin(uid)

    # отправка админам бота сообщения с заказом
    for admin_uid in ADMINS:
        await bot.send_message(admin_uid, order)

    # добавление в таблицу заказов
    db.add_order(uid)
    # Очистка корзины
    db.delete_cart(message.from_user.id)

