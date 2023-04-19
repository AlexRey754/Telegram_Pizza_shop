from aiogram.dispatcher.filters.state import StatesGroup, State

class Register(StatesGroup):
    name = State()
    tel_number = State()

class AddPosition(StatesGroup):
    name = State()
    description = State()
    price = State()

class ChangePrice(StatesGroup):
    id = State()
    price = State()

class OrderState(StatesGroup):
    adress = State()


