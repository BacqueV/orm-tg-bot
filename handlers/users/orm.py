from aiogram import types
from data.config import ADMINS
from loader import dp, db

from states.orm_states import OrmPanel, CreateTable
from keyboards.default import admin_panel
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(text='/orm', user_id=ADMINS)
async def show_admin_panel(message: types.Message):
    await message.answer(
        'Welcome to ORM panel using <i>sqlite3</i>\n\n'
        '/users - list all users in DB\n'
        '/clean_db - cleans <i>Users</i> table\n\n'
        'You can select a table from the list by entering its id',
        reply_markup=admin_panel.markup_orm_options
    )
    await OrmPanel.main.set()


# --- Creating Table | Start ---
@dp.message_handler(text='Create table', state=OrmPanel.main)
async def creating_initial_config(message: types.Message, state: FSMContext):
    await message.answer(
        'Set a name for the table',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.finish()
    await CreateTable.table_name.set()


# Saving tables name | Asking for setting columns name
@dp.message_handler(state=CreateTable.table_name)
async def save_table_name(message: types.Message, state: FSMContext):
    table_name = message.text
    await state.set_data(
        {
            'table_name': table_name,
            'fields': []
        }
    )
    await CreateTable.column_name.set()
    await message.answer('Set a name for the column')


# Saving columns name | Asking for setting columns type
@dp.message_handler(state=CreateTable.column_name)
async def save_column_name(message: types.Message, state: FSMContext):
    column_name = message.text
    await state.update_data(
        {
            'column_name': column_name
        }
    )
    await CreateTable.column_type.set()
    await message.answer(f'Choose type for column <i>{column_name}</i>',
                         reply_markup=admin_panel.markup_type_options)


# Saving columns type | Asking for next action
@dp.message_handler(text=('INTEGER', 'TEXT', 'REAL'), state=CreateTable.column_type)
async def save_column_type(message: types.Message, state: FSMContext):
    column_type = message.text

    data = await state.get_data()
    column_name = data.get('column_name')
    fields = data.get('fields')

    if fields is not None:
        fields.append({
            "column_name": column_name,
            'column_type': column_type
        })

    del data['column_name']
    await state.set_data(data)

    await CreateTable.column_name.set()
    await message.answer('Choose next action, or continue creating',
                         reply_markup=admin_panel.markup_next_action)


# Climax processing
# Create options is in another file /handlers/users/create_db.py
@dp.message_handler(text='Interrupt', state=CreateTable.column_name)
async def climax_actions(message: types.Message, state: FSMContext):
    # users next action
    will = message.text

    if will == 'Interrupt':
        await state.finish()
        await OrmPanel.main.set()
        await message.answer('<b><i>Creating table interrupted</i></b>',
                             reply_markup=admin_panel.markup_orm_options)
