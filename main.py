import time
import types

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import config

storage = MemoryStorage()

bot = Bot(token=config.TOKEN)

dispatcher = Dispatcher(bot=bot, storage=storage)

ADMIN_IDS = [int(config.ADMIN_ID)]


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)
