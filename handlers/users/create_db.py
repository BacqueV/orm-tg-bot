from aiogram import types
from loader import dp, db
from aiogram.dispatcher import FSMContext

from keyboards.default.admin_panel import markup_orm_options
from states.orm_states import OrmPanel, CreateTable


@dp.message_handler(text='Create', state=CreateTable.continue_or_not)
async def create_db(message: types.Message, state: FSMContext):

    # extracting data from state
    data = await state.get_data()

    # cratind db
    print(data)
    db.create_custom_table(data)

    # setting main state
    await OrmPanel.main.set()
    await message.answer('<b><i>Table successfully created</i></b>', reply_markup=markup_orm_options)
