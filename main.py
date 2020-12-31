import os
import re
import io
import logging
import asyncio
import numpy as np
from time import gmtime, strftime, localtime, sleep
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from states import TTStatsForm
from do import do_remember_user_start


root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('tik_tok_stats.log', 'w', 'utf-8')
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
root_logger.addHandler(handler)

loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage, loop=loop)


@dp.message_handler(commands=['start'])
async def send_start_command(message: types.Message):
    """Отправляет приветственное сообщение"""
    await do_remember_user_start(message)
    try:
        text_choices = (0, 1) # 0 - just text | 1 - sub please text
        #choice = np.random.choice(a=text_choices, size=1, replace=True, p=[0.8, 0.2])[0]
        choice = 1
        if choice == 0:
            start_text = "1. просто текст"
            await message.answer(start_text, disable_notification=True)

            instruction_text = "инструкция репорт1"
            await message.answer(instruction_text, disable_notification=True)
            #await TTStatsForm.nickname.set()
        elif choice == 1:
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Подписаться", url="https://www.google.com/")
            call_button = types.InlineKeyboardButton(text="Я подписан", callback_data="sub_first")
            keyboard.add(url_button)
            keyboard.add(call_button)
            
            start_text = "2. текст с призывом подписаться"
            await message.answer(start_text, reply_markup=keyboard, disable_notification=True)
            await TTStatsForm.is_sub_first.set()
    except:
        await message.answer("Произошла ошибка", disable_notification=True)


@dp.callback_query_handler(lambda callback_query: True, state=TTStatsForm.is_sub_first)
async def is_sub_first_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """После нажатия кнопки 'Я подписан' отправляет инструкцию репорт1"""
    try:
        if callback_query.data == "sub_first":
            instruction_text = "инструкция репорт1 - никнейм"
            await callback_query.message.answer(instruction_text, disable_notification=True)
            await TTStatsForm.nickname.set()
        else:
            await callback_query.message.answer("Чего нажал?", disable_notification=True)
    except:
        await callback_query.message.answer("Произошла ошибка", disable_notification=True)


@dp.message_handler(state=TTStatsForm.nickname)
async def nickname_message_handler(message: types.Message):
    """Получает никнейм, проверяет его и делает запрос на сервер"""
    try:
        nickname = message.text
        if not bool(re.search('[а-яА-Я]', nickname)):
            await message.answer("Запрос на сервер..", disable_notification=True)
            await message.answer("репорт1", disable_notification=True)

            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Подписаться", url="https://www.google.com/")
            call_button = types.InlineKeyboardButton(text="Я подписан", callback_data="sub_second")
            keyboard.add(url_button)
            keyboard.add(call_button)
            await message.answer("Подпишитесь на канал для репорт2", reply_markup=keyboard, disable_notification=True)
            await TTStatsForm.is_sub_second.set()
        else:
            await message.answer("Отправьте корректный никнейм", disable_notification=True)
            await TTStatsForm.nickname.set()
    except:
        await message.answer("Произошла ошибка", disable_notification=True)


@dp.callback_query_handler(lambda callback_query: True, state=TTStatsForm.is_sub_second)
async def is_sub_second_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """После нажатия кнопки 'Я подписан' отправляет инструкцию репорт2"""
    try:
        if callback_query.data == "sub_second":
            instruction_text = "инструкция репорт2 и видео"
            await callback_query.message.answer("отправь первый файл")
            await callback_query.message.answer(instruction_text, disable_notification=True)
            await TTStatsForm.file1.set()
        else:
            await callback_query.message.answer("Чего нажал?", disable_notification=True)
    except:
        await callback_query.message.answer("Произошла ошибка", disable_notification=True)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=TTStatsForm.file1)
async def file_1_handler(message: types.Message, state: FSMContext):
    try:
        is_valid = True
        if is_valid:
            await state.update_data(file1=message.document.file_id)
            await message.answer("теперь второй файл", disable_notification=True)
            await TTStatsForm.file2.set()
        else:
            await message.answer("Пришли нормальный файл1")
            await TTStatsForm.file1.set()
    except:
        await message.answer("Произошла ошибка", disable_notification=True)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=TTStatsForm.file2)
async def file_2_handler(message: types.Message, state: FSMContext):
    try:
        is_valid = True
        if is_valid:
            await state.update_data(file1=message.document.file_id)
            await message.answer("репорт2", disable_notification=True)
            await state.reset_state(with_data=True)
        else:
            await message.answer("Пришли нормальный файл2")
            await TTStatsForm.file2.set()
    except:
        await message.answer("Произошла ошибка", disable_notification=True)



@dp.message_handler(commands=['help'])
async def send_help_command(message: types.Message):
    """Отправляет вспомогательное сообщение"""
    help_text = "помощь"

    await message.answer(help_text, disable_notification=True)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)