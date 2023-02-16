import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd


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
