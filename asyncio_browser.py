import asyncio

from pyppeteer import browser
from pyppeteer import page
from pyppeteer import launch
import random
import string

import time


class WebBrowser:
    def __init__(self):
        self.browser: browser.Browser
        self.page: page.Page
        self.phone: str

    async def initialize(self):
        try:
            #self.browser = await launch(options={"args": ['--no-sandbox']})
            self.browser = await launch(options={"headless": False})
            self.page = await self.browser.newPage()
            print(type(self.browser), type(self.page))
        except Exception as e:
            print(e)
            return False
        print('OK')
        return True

    async def close(self):
        try:
            await self.browser.close()
        except Exception as e:
            print(e)

    async def get_page(self):
        try:
            print(1)
            self.page.setDefaultNavigationTimeout(0)
            await self.page.goto('https://lk.kopilkaclub.ru/login')
            await asyncio.sleep(5)
            return True
        except Exception as e:
            print(e)

    async def input_login(self):
        try:
            await asyncio.sleep(1)
            print(2)
            login = ''.join(random.choice(string.ascii_letters) for _ in range(random.randrange(8, 16)))
            await self.page.type('input#login-form_login', login)
            await asyncio.sleep(2)

            return True
        except Exception as e:
            print('error: ' + str(e))
            return False, e

    async def input_password(self):
        try:
            await asyncio.sleep(1)
            print(3)
            password = ''.join(random.choice(string.ascii_letters) for _ in range(random.randrange(8, 16)))
            await self.page.type('input#login-form_password', password)
            await asyncio.sleep(2)

            return True
        except Exception as e:
            print('error: ' + str(e))
            return False, e

    async def press_btc(self):
        try:
            await asyncio.sleep(1)
            btn = await self.page.querySelector('div.ant-form-item-control-input-content > button.ant-btn-primary')
            await btn.press('Enter')
            await asyncio.sleep(2)

            errors = await self.page.querySelectorAll('div.ant-notification-notice-message')
            if len(errors):
                await self.page.reload()
                await asyncio.sleep(3)
                return False, 'not'

            return True, 'ok'
        except Exception as e:
            print('error: ' + str(e))
            return False, 'error'
