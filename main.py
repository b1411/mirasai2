import asyncio
import requests
import logging
import json
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет я MIRAS AI")


@dp.message()
async def echo(message: Message):
    req = {
        "message": message.text,
        "contactId": message.from_user.id
    }
    res = requests.post('https://jasik.alwaysdata.net/mirasaitg', json=req).json()

    await message.answer(res['message'])


async def main():
    bot = Bot(token="7156102554:AAF-37RMlJjv_EGPVJrt8OPxo13ZLvXCFFM",
              parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
