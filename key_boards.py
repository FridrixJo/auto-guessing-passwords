from aiogram import types


def inline_markup_menu(user_id: int, db):
    kb = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Запустить поиск ✅', callback_data='start')

    status = db.get_status(user_id=user_id)
    if status == 1:
        btn1 = types.InlineKeyboardButton('Остановить поиск ⛔', callback_data='stop')

    btn2 = types.InlineKeyboardButton('Статистика', callback_data='statistics')

    kb.add(btn1, btn2)

    return kb


def inline_markup_back(text):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text + ' ↩️', callback_data='back')

    kb.add(btn1)

    return kb
