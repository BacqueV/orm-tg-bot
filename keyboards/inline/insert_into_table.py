from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_insert_data = InlineKeyboardButton(text='Insert data', callback_data='insert_data')
markup_insert_data = InlineKeyboardMarkup().insert(btn_insert_data)
