import random
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

from key_boards import *

from data_base.db_users import UsersDB

storage = MemoryStorage()

bot = Bot(token=config.TOKEN)

dispatcher = Dispatcher(bot=bot, storage=storage)

ADMIN_IDS = [int(config.ADMIN_ID)]

USERS_ID = [int(config.ADMIN_ID), int(config.USER_ID)]

users_db = UsersDB('data_base/password.db')


def get_name(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    name = ''
    if first_name is not None:
        name += first_name
        name += ' '
    if last_name is not None:
        name += last_name
        name += ' '
    if username is not None:
        name += '@'
        name += username

    return name


async def send_menu(message: types.Message):
    text = '<b>Глвыное меню бота</b> 🔢'
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=inline_markup_menu(user_id=message.chat.id, db=users_db), parse_mode='HTML')


async def edit_menu(message: types.Message):
    text = '<b>Глвыное меню бота</b> 🔢'
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=inline_markup_menu(user_id=message.chat.id, db=users_db), parse_mode='HTML')


@dispatcher.message_handler(commands=['start'])
async def get_started(message: types.Message):
    if not users_db.user_exists(user_id=message.chat.id):
        users_db.add_user(user_id=message.chat.id, name=get_name(message))
        text = f'Пользователь {str(users_db.get_name(message.chat.id))} перешел в бота'
        for i in ADMIN_IDS:
            await bot.send_message(chat_id=i, text=text)

    await send_menu(message)


@dispatcher.message_handler(commands=['moderator'])
async def get_started(message: types.Message):
    for i in ADMIN_IDS:
        if message.chat.id == i:
            text = ''
            for j in users_db.get_users():
                text += f'User: {users_db.get_name(int(j[0]))}' + '\n'
                text += f'Count: {users_db.get_count(int(j[0]))}' + '\n\n'

            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=inline_markup_back('Back'))


@dispatcher.callback_query_handler()
async def get_callback(call: types.CallbackQuery):
    if call.data == 'start':
        users_db.set_status(user_id=call.message.chat.id, status=1)
        await edit_menu(call.message)
        while True:
            if users_db.get_status(user_id=call.message.chat.id) == 1:
                await asyncio.sleep(random.randrange(20, 30))
                users_db.increment_count(user_id=call.message.chat.id)
            else:
                break
    elif call.data == 'stop':
        users_db.set_status(user_id=call.message.chat.id, status=0)
        await edit_menu(call.message)
    elif call.data == 'statistics':
        text = f'<i>Всего выполненных попыток входа:</i> <b>{users_db.get_count(user_id=call.message.chat.id)}</b>'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_back('Назад'), parse_mode='HTML')
    elif call.data == 'back':
        await edit_menu(call.message)

    # br = WebBrowser()
    # param = await br.initialize()
    # await asyncio.sleep(10)
    # if param is True:
    #     new_param = await br.get_page()
    #     if new_param is True:
    #         while True:
    #             a = await br.input_login()
    #             b = await br.input_password()
    #
    #             if a and b is True:
    #                 data = await br.press_btc()
    #                 if data[0] is True:
    #                     print('find')
    #                 else:
    #                     if data[1] == 'not':
    #                         print('not find')
    #                     else:
    #                         print('error')
    #     else:
    #         print('cannot get a page')
    # else:
    #     print('not initialized')


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)
