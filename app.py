import types

from sphinx.util import requests


import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5753480937:AAG7bQbpo2hwpd201d4FrIrK6wjx9xHGFz0'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Salom!\nBu bot Rasulbek tomonidan yaratildi\nMenda o'zbek tilidagi oyatni topishingiz mumkin\nfoydalanish 1-5 yani 1-sura 5- oyat.")



@dp.message_handler()
async def echo(message: types.Message):
    for i in range(len(message.text) - 1):
        if message.text[i] == '-':
            sura = (message.text[:i])
            oyat = (message.text[i + 1:])


    #
    # sura = int(message.text[0]+message.text[1])
    # oyat = int(message.text[2]+message.text[3])

    url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-muhammadsodikmu/{sura}/{oyat}.json'
    response = requests.get(url)



    await message.answer(response.json()['text'])
    # await message.answer(type(sura))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)