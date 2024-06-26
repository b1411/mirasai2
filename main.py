import asyncio
import requests
import logging
import json
import sys
import time

import redis
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет я MIRAS AI")


@dp.message(Command("end"))
async def end(message: Message):
    res = requests.post('https://jasik.alwaysdata.net/clear-ig-session',
                        json={"contactId": f'{str(message.chat.id)}miras'})

    if res.status_code == 200:
        await message.answer("Ваша сессия прервана, пожалуйста начните сначала")

    else:
        await message.answer("Что-то пошло не так")


@dp.message()
async def echo(message: Message):
    try:
        res = requests.post(
            'https://jasik.alwaysdata.net/mirasaitg', data=json.dumps({
                "message": message.text,
                "contactId": f'{str(message.chat.id)}miras'
            }), headers={"Content-Type": "application/json"})

        if res.status_code == 200:
            data = res.json()

        else:
            raise Exception(
                f"Status code: {res.status_code}, response: {res.text}")

        await message.answer(data['message'])

    except Exception as e:
        logging.error(e)
        await message.answer("Что-то пошло не так")


async def main():
    bot = Bot(token="7156102554:AAF-37RMlJjv_EGPVJrt8OPxo13ZLvXCFFM",
              parse_mode=ParseMode.MARKDOWN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
