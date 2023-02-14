import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from states.ORM import OrmPanel, CreateTable
from keyboards.default import admin_panel
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(text="/users", user_id=ADMINS, state='*')
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    user_id = []
    name = []
    for user in users:
        user_id.append(user[3])
        name.append(user[1])
    data = {
        "Telegram ID": user_id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
        await bot.send_message(message.chat.id, df)


@dp.message_handler(text="/advert", user_id=ADMINS, state='*')
async def send_ad_to_all(message: types.Message):
    """Function requires at least 1 user in DB"""
    users = db.select_all_users()
    for user in users:
        user_id = user[3]
        await bot.send_message(chat_id=user_id, text="Join @tessssssssssts1")
        await asyncio.sleep(0.05)


@dp.message_handler(text="/clean_db", user_id=ADMINS, state='*')
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Database cleared!")


@dp.message_handler(text='/orm', user_id=ADMINS)
async def show_admin_panel(message: types.Message):
    await message.answer(
        'Welcome to ORM panel using <i>sqlite3</i>\n\n'
        '/users - list all users in DB\n'
        '/clean_db - cleans <i>Users</i> table',
        reply_markup=admin_panel.markup_orm_options
    )
    await OrmPanel.main.set()


@dp.message_handler(text='List tables', state=OrmPanel.main)
async def list_tables(message: types.Message):
    tables = db.show_tables()
    text = '<b>All existing tables</b>\n\n'

    if len(tables) == 1:
        await message.answer(f'{text}{tables[0][0]}')
    else:
        for table in tables[0]:
            table_id = 1
            text += f'{table_id}. {table}\n'
            table_id += 1
        await message.answer(text)


# --- Creating Table | Start ---
@dp.message_handler(text='Create table', state=OrmPanel.main)
async def creating_initial_config(message: types.Message, state: FSMContext):
    await message.answer(
        'Set a name for the table',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_data(
        {   # for parameter collection
            'table_rows_data': list()
        }
    )
    await CreateTable.table_name.set()


# Saving tables name | Asking for setting columns name
@dp.message_handler(state=CreateTable.table_name)
async def save_table_name(message: types.Message, state: FSMContext):
    table_name = message.text
    await state.set_data(
        {
            'table_name': table_name
        }
    )
    await CreateTable.column_name.set()
    await message.answer('Set a name for the column')


# Saving columns name | Asking for setting columns type
@dp.message_handler(state=CreateTable.column_name)
async def save_column_name(message: types.Message, state: FSMContext):
    column_name = message.text
    await state.set_data(
        {
            'column_name': column_name
        }
    )
    await CreateTable.column_type.set()
    await message.answer(f'Choose type for column <i>{column_name}</i>', reply_markup=admin_panel.markup_type_options)


# Saving columns type | Asking for next action
@dp.message_handler(text=('Integer', 'Text'), state=CreateTable.column_type)
async def save_column_type(message: types.Message, state: FSMContext):
    column_type = message.text
    await state.set_data(
        {
            'column_type': column_type
        }
    )
    await CreateTable.continue_or_not.set()
    await message.answer('What would you like to do?', reply_markup=admin_panel.markup_ask_for_continue)


# Climax processing
@dp.message_handler(text=('Interrupt', 'Create'), state=CreateTable.continue_or_not)
async def climax_actions(message: types.Message, state: FSMContext):
    # users next action
    will = message.text

    if will == 'Interrupt':
        await state.finish()
        await message.answer('<b><i>Creating table interrupted</i></b>', reply_markup=admin_panel.markup_orm_options)
    elif will == 'Create':
        # ADD HERE SQL FUNCTION
        await message.answer('<b><i>Table successfully created</i></b>', reply_markup=admin_panel.markup_orm_options)
    else:
        await message.answer('<b><i>Choose the correct option</i></b>')


# Parameter collection implementation
@dp.message_handler(text='Continue', state=CreateTable.continue_or_not)
async def continue_specifying(message: types.Message, state: FSMContext):
    await CreateTable.column_name.set()
    await message.answer('Set a name for the column', reply_markup=ReplyKeyboardRemove())
