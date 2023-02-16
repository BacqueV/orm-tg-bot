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
async def creating_initial_config(message: types.Message):
    await message.answer(
        'Set a name for the table',
        reply_markup=ReplyKeyboardRemove()
    )
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
    await message.answer(f'Choose type for column <i>{column_name}</i>', reply_markup=admin_panel.markup_type_options)


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
        await CreateTable.create_table.set()
        await message.answer('<b><i>Table successfully created</i></b>', reply_markup=admin_panel.markup_orm_options)
    else:
        await message.answer('<b><i>Choose the correct option</i></b>')


# Parameter collection implementation
@dp.message_handler(text='Continue', state=CreateTable.continue_or_not)
async def continue_specifying(message: types.Message):
    await CreateTable.column_name.set()
    await message.answer('Set a name for the column', reply_markup=ReplyKeyboardRemove())
