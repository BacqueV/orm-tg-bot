from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# options for db control
list_tables = KeyboardButton('List tables')
create_table = KeyboardButton('Create table')
markup_orm_options = ReplyKeyboardMarkup(resize_keyboard=True).add(list_tables, create_table)

# row type options
type_integer = KeyboardButton('INTEGER')
type_real = KeyboardButton('REAL')
type_text = KeyboardButton('TEXT')
markup_type_options = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(type_integer, type_real, type_text)


# ask for continuing process
btn_interrupt = KeyboardButton('Interrupt')
btn_create = KeyboardButton('Create')
btn_continue = KeyboardButton('Continue')
markup_ask_for_continue = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_continue).add(btn_interrupt, btn_create)
