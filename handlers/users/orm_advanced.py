from aiogram import types
from loader import dp, db

from states.orm_states import OrmPanel
from aiogram.dispatcher import FSMContext
from keyboards.inline.insert_into_table import markup_insert_data

ENTER_THE_CORRECT_VALUE = 'Enter the correct value!'
THERE_IS_NO_SUCH_A_DATA = 'There is no such a data!'


# there is no reason for you to check if the user is an admin
@dp.message_handler(text='List tables', state=OrmPanel.main)
async def list_tables(message: types.Message, state: FSMContext):
    tables = db.show_tables()
    text = '<b>All existing tables</b>\n\n'

    if len(tables) == 1:
        await message.answer(f'{text}{tables[0][0]}')
    else:
        table_id = 1

        id_and_tables = list()

        for table in tables:
            id_and_tables.append((table_id, table[0]))

            text += f'{table_id}. {table[0]}\n'
            table_id += 1

        await state.set_data(
            {
                'id_and_tables': id_and_tables
            }
        )
        await message.answer(text + '\nYou can select a table from the list by entering its id')


@dp.message_handler(state=OrmPanel.main)
async def show_table_details(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_and_tables = data['id_and_tables']

    table_name = str()
    table_info = list()

    try:
        table_id = int(message.text)
    except ValueError:
        await message.reply(ENTER_THE_CORRECT_VALUE)
        return 1

    if table_id > 0:
        for table in id_and_tables:
            # searching a table
            if table_id == table[0]:
                table_name = table[1]
                table_info = db.show_table_details(table_name)
                break
    else:
        await message.reply(ENTER_THE_CORRECT_VALUE)
        return 1

    if not table_info:
        await message.reply(THERE_IS_NO_SUCH_A_DATA)
        return 1

    information_message = f"""<b>Table: {table_name}</b>\n\n"""
    for item in table_info:
        cid = item[0]
        name = item[1]
        row_type = item[2]
        notnull = item[3]
        dflt_value = item[4]
        pk = item[5]

        information_message += f"column id: {cid}\n" \
                               f"name: {name}\n" \
                               f"row type: {row_type}\n" \
                               f"not null: {bool(notnull)}\n" \
                               f"default value: {dflt_value}\n" \
                               f"primary key: {bool(pk)}\n\n"

    data.update(
        {
            'table_id': table_id
        }
    )
    await state.set_data(data)
    await message.answer(information_message, reply_markup=markup_insert_data)


@dp.callback_query_handler(text='insert_data', state=OrmPanel.main)
async def insert_data(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    table_id = data['table_id']
    id_of_tables = data['id_of_tables']

    for table in id_of_tables:
        if table_id == table[0]:
            await call.message.answer(f'You have chosen a <b>{table[1]}</b> table')
            break
