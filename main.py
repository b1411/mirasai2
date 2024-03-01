import asyncio
import requests
import logging
import json
import sys
import time

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет я MIRAS AI")


@dp.message()
async def echo(message: Message):
    global last_message_time
    current_time = time.time()
    if current_time - last_message_time >= 3600:
        res = requests.post('https://jasik.alwaysdata.net/clear-ig-session',
                            json={"contactId": message.from_user.username}).json()
        await message.answer("Ваша сессия прервана, пожалуйста начните сначала")
        last_message_time = current_time
        return

    req = {
        "message": message.text,
        "contactId": message.from_user.username
    }
    res = requests.post(
        'https://jasik.alwaysdata.net/mirasaitg', json=req).json()

    last_message_time = current_time

    await message.answer(res['message'])


@dp.message(Command("end"))
def end(message: Message):
    res = requests.post('https://jasik.alwaysdata.net/clear-ig-session',
                        json={"contactId": message.from_user.username}).json()
    if res['status'] == 200:
        message.answer("Ваша сессия прервана, пожалуйста начните сначала")
    else: 
        message.answer("Ошибка")


async def main():
    bot = Bot(token="7156102554:AAF-37RMlJjv_EGPVJrt8OPxo13ZLvXCFFM",
              parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
