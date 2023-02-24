from aiogram import types
from loader import dp, db

from states.orm_states import OrmPanel
from aiogram.dispatcher import FSMContext


# there is no reason for you to check if the user is an admin
@dp.message_handler(text='List tables', state=OrmPanel.main)
async def list_tables(message: types.Message, state: FSMContext):

    tables = db.show_tables()
    text = '<b>All existing tables</b>\n\n'

    await state.set_data(
        {
            'id_of_tables': list()
        }
    )

    if len(tables) == 1:
        await message.answer(f'{text}{tables[0][0]}')
    else:
        table_id = 1

        data = await state.get_data()
        tables_and_id = data.get('id_of_tables')

        for table in tables:
            tables_and_id.append((table_id, table[0]))

            text += f'{table_id}. {table[0]}\n'
            table_id += 1

        await state.set_data(data)
        print(data)
        await message.answer(text)


@dp.message_handler(state=OrmPanel.main)
async def show_table_details(message: types.Message, state: FSMContext):
    data = await state.get_data()

    table_id = int(message.text)
    for table in data['id_of_tables']:
        if table_id == table[0]:

            table_name = table[1]
            table_info = db.show_table_details(table_name)

            break
    
    msg = f"""<b>Table: {table_name}</b>\n\n"""
    for item in table_info:
        cid = item[0]
        name = item[1]
        row_type = item[2]
        notnull = item[3]
        dflt_value = item[4]
        pk = item[5]

        msg += f"cid: {cid}\n" \
            f"name: {name}\n" \
            f"row type: {row_type}\n" \
            f"not null: {bool(notnull)}\n" \
            f"default value: {dflt_value}\n" \
            f"primary key: {bool(pk)}\n\n"

    await message.answer(msg)
