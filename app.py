from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.set_bot_commands import set_default_commands
from utils.db_api import db
from data.upload_products import upload_all

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды

    await set_default_commands(dispatcher)

    ''' Откомментировать для заполнения базы'''
    upload_all(False)
if __name__ == '__main__':
    db.create_db()
    executor.start_polling(dp, on_startup=on_startup)

