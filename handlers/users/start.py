import sqlite3

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    username = message.from_user.username
    # add user to database
    try:
        if username is None:
            db.add_user(
                user_id=message.from_user.id,
                name=name,
                username='None'
            )
        else:
            db.add_user(
                user_id=message.from_user.id,
                name=name,
                username=username
            )
        await message.answer(f"{name}, Welcome!", reply_markup=ReplyKeyboardRemove())
        # inform the administration
        count = db.count_users()[0]
        msg = f"{message.from_user.full_name} the user has been added to the database" \
              f"\nDatabase has {count} users"
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except sqlite3.IntegrityError:
        await bot.send_message(chat_id=ADMINS[0], text=f"{name} has already been in database")
        await message.answer(f"{name}, Welcome!", reply_markup=ReplyKeyboardRemove())
