import time
import types

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import asyncio

from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import config

from asyncio_browser import WebBrowser

storage = MemoryStorage()

bot = Bot(token=config.TOKEN)

dispatcher = Dispatcher(bot=bot, storage=storage)

ADMIN_IDS = [int(config.ADMIN_ID)]


@dispatcher.message_handler(commands=['start'])
async def get_started(message: types.Message):
    br = WebBrowser()
    param = await br.initialize()
    await asyncio.sleep(10)
    if param is True:
        new_param = await br.get_page()
        if new_param is True:
            while True:
                a = await br.input_login()
                b = await br.input_password()

                if a and b is True:
                    data = await br.press_btc()
                    if data[0] is True:
                        print('find')
                    else:
                        if data[1] == 'not':
                            print('not find')
                        else:
                            print('error')
        else:
            print('cannot get a page')
    else:
        print('not initialized')


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)
