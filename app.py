import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5857956690:AAHHeq_vN12_41DoSqQfGC-ck8aADHakHuM'

bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'
    muassasa = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.name.set()

    await message.answer(
        "Assalomu Alekum Bu AKT va AXI tomonidan\n\nKonferensiya registratsiya bot\n\n Familya Ism Sharifizni kiriting")


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.answer("Telefon raqamizni kiriting\n Masalan: 991110011")


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit() or not len(message.text) == 9, state=Form.age)
async def process_age_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.reply("Noto'g'ri.\nBu yerga raqam kiriting (9 ta)")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(age=int(message.text))

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("SUMO robotlar jangi", "CSGO", "Ilmiy ishlanmalar")

    await message.answer("Qaysi kiber sport turini tanlaysiz?", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["SUMO robotlar jangi", "CSGO", "Ilmiy ishlanmalar"],
                    state=Form.gender)
async def process_gender_invalid(message: types.Message):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    return await message.reply("Siz notog'ri kiritdingiz iltimos to'g'ri bo'limni tanlang")


@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await Form.next()
    # Remove keyboard

    # And send message

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, )
    markup.add("QK Akademiyasi ", "II Akademiyasi", "MG Intituti", "AKT va AXI Inistituti", "CHirchiq OTQMBYu","Qashqadaryo HABYu")

    await message.answer("Muossasa Nomini kiriting", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["QK Akademiyasi ", "II Akademiyasi", "MG Intituti", "AKT va AXI Inistituti", "CHirchiq OTQMBYu","Qashqadaryo HABYu"],
                    state=Form.muassasa)
async def process_gender_invalid(message: types.Message):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    return await message.reply("Siz notog'ri kiritdingiz iltimos to'g'ri bo'limni tanlang")


@dp.message_handler(state=Form.muassasa)
async def process_muassasa(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, )
    markup.add("start")
    async with state.proxy() as data:
        data['muassasa'] = message.text
        f = open("users.txt", "a")
        f.write(
            f"{data['name']}\n   id:{message.chat.id}\n   tn:{data['age']}\n   {data['gender']}\n   {data['muassasa']}\n")
        f.close()

        await bot.send_message(

            984568970,
            md.text(
                md.text('Katta Raxmat:         ', md.bold(data['name'])),
                md.text('chat id :                   ', message.chat.id),

                md.text('Naqamingiz:           ', md.code(data['age'])),
                md.text('Kiber sport turi:     ', data['gender']),
                md.text('Muassasa nomi:     ', data['muassasa']),
                sep='\n',

            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        markup = types.ReplyKeyboardRemove()

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Katta Raxmat:           ', md.bold(data['name'])),
                md.text('Naqamingiz:             ', md.code(data['age'])),
                md.text('Kiber sport turi:       ', data['gender']),
                md.text('Muassasa nomi:       ', data['muassasa']),
                sep='\n',
            ),

            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation

    await message.answer("Agar malumotlarni o'zgartirishni hohlasangiz  /start ni yuboring", reply_markup=markup)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
