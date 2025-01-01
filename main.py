import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import Message
from chekWord import checkWord
from transliterate import to_cyrillic, to_latin


#this is bot token
BOT_TOKEN = ""
TOKEN = BOT_TOKEN

dp = Dispatcher()


#this is start command
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f" Assalomu alaykum, {html.bold(message.from_user.full_name)}\nIMLOBOTga hohlaganingizni yozing!!!")

#this is privacy command
@dp.message(Command(commands=["privacy"]))
async def privacy(message: Message):
    await message.answer(f"Quyidagi link ustiga bosing: [privacy link](https://docs.google.com/document/d/1KI_BSOVnu7YMB_sWzFDXq4rPM8syp3s3-B4joOazVmo/edit?usp=sharing)",parse_mode="Markdown")

#this is IMLO handler
@dp.message()
async def imlobot(message: Message) -> None:
    words = message.text.split()
    for word in words:
        if word.isascii() and word.isalpha():
            word = to_cyrillic(word)
            result = checkWord(word)
            if result['available']:
                word = to_latin(word)
                response = f"✅ {word.capitalize()}"
            else:
                word = to_latin(word)
                response = f"❌{word.capitalize()}\n"
                for text in result['matches']:
                    text = to_latin(text)
                    response += f"✅ {text.capitalize()}\n"
            await message.answer(response)


        else:
            word = word
            result = checkWord(word)
            if result['available']:
                response = f"✅ {word.capitalize()}"
            else:
                response = f"❌{word.capitalize()}\n"
                for text in result['matches']:
                    response += f"✅ {text.capitalize()}\n"
            await message.answer(response)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())    
