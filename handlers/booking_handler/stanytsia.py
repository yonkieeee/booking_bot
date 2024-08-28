import asyncio
import requests
import re
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import bots
import keyboards
from datetime import datetime
import pytz
from calendars import STANYTSIA_TEAMUP_API_KEY, STANYTSIA_TEAMUP_CALENDAR_ID
from . import db_booking
from .booking_menu import fetch_calendar_events, add_calendar_event, check_event_conflicts
from handlers.start_menu import user_db

router = Router()
bot = Bot(bots.main_bot)


class Stanytsia_Bookingreg(StatesGroup):
    stanytsia_booking_name = State()
    stanytsia_number_of_room = State()
    stanytsia_day = State()
    stanytsia_start_time = State()
    stanytsia_end_time = State()


@router.callback_query(F.data == "stanytsia")
async def bookstanytsia(callback: types.CallbackQuery):
    await callback.message.answer("Перед натисканням на кнопку 'Реєстрація бронювання' переглянь графік", reply_markup=keyboards.stanytsiakb)

@router.callback_query(F.data == "RegistrateBookingStanytsia")
async def reg_stanytsia_one(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Stanytsia_Bookingreg.stanytsia_booking_name)
    await bot.send_message(chat_id=callback.from_user.id, text="Введіть назву події")

@router.message(Stanytsia_Bookingreg.stanytsia_booking_name)
async def reg_stanytsia_two(message: Message, state: FSMContext):
    await state.update_data(stanytsia_booking_name=message.text)
    await state.set_state(Stanytsia_Bookingreg.stanytsia_number_of_room)
    await message.answer("Оберіть номер кімнати", reply_markup=keyboards.room_inline)

@router.callback_query(Stanytsia_Bookingreg.stanytsia_number_of_room)
async def reg_stanytsia_three(callback: CallbackQuery, state: FSMContext):
    await state.update_data(stanytsia_number_of_room=callback.data)
    await state.set_state(Stanytsia_Bookingreg.stanytsia_day)
    await callback.message.answer("Введіть день у форматі РРРР-ММ-ДД. Наприклад: 2024-05-20")

@router.message(Stanytsia_Bookingreg.stanytsia_day)
async def reg_stanytsia_four(message: Message, state: FSMContext):
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(date_pattern, message.text):
        await message.answer("Неправильний формат дати. Будь ласка, введіть день у форматі РРРР-ММ-ДД. Наприклад: 2024-05-20")
        return
    await state.update_data(stanytsia_day=message.text)
    await state.set_state(Stanytsia_Bookingreg.stanytsia_start_time)
    await message.answer("Введіть час початку у форматі ГГ:ХХ. Наприклад 15:00")

@router.message(Stanytsia_Bookingreg.stanytsia_start_time)
async def reg_stanytsia_five(message: Message, state: FSMContext):
    time_pattern = r"^\d{2}:\d{2}$"
    if not re.match(time_pattern, message.text):
        await message.answer("Неправильний формат часу. Будь ласка, введіть час у форматі ГГ:ХХ. Наприклад 15:00")
        return
    await state.update_data(stanytsia_start_time=message.text)
    await state.set_state(Stanytsia_Bookingreg.stanytsia_end_time)
    await message.answer("Введіть час закінчення у форматі ГГ:ХХ. Наприклад 16:00")


@router.message(Stanytsia_Bookingreg.stanytsia_end_time)
async def reg_stanytsia_six(message: Message, state: FSMContext):
    time_pattern = r"^\d{2}:\d{2}$"
    if not re.match(time_pattern, message.text):
        await message.answer("Неправильний формат часу. Будь ласка, введіть час у форматі ГГ:ХХ. Наприклад 16:00")
        return
    await state.update_data(stanytsia_end_time=message.text)
    data = await state.get_data()
    
    room_mapping = {"303": 13281316, "201": 13281315, "206": 13281315, "208": 13281315}
    if data["stanytsia_number_of_room"] in room_mapping:
        data["stanytsia_number_of_room"] = room_mapping[data["stanytsia_number_of_room"]]
    else:
        await message.answer("Ви ввели неправильний номер кімнати. Зареєструйте бронювання ще раз.")
        await state.set_state(Stanytsia_Bookingreg.stanytsia_booking_name)
        await bot.send_message(chat_id=message.from_user.id, text="Введіть назву події")
        return

    local_tz = pytz.timezone("Europe/Kiev")
    start_datetime = local_tz.localize(datetime.strptime(f'{data["stanytsia_day"]} {data["stanytsia_start_time"]}', '%Y-%m-%d %H:%M')).astimezone(pytz.utc)
    end_datetime = local_tz.localize(datetime.strptime(f'{data["stanytsia_day"]} {data["stanytsia_end_time"]}', '%Y-%m-%d %H:%M')).astimezone(pytz.utc)

    print(f"Checking conflicts for room {data['stanytsia_number_of_room']} from {start_datetime.isoformat()} to {end_datetime.isoformat()}")
    if await check_event_conflicts(data["stanytsia_number_of_room"], start_datetime.isoformat(), end_datetime.isoformat(), STANYTSIA_TEAMUP_CALENDAR_ID, STANYTSIA_TEAMUP_API_KEY):
        await message.answer("На цей час у вибраній кімнаті вже є подія. Виберіть інший час.")
        await state.set_state(Stanytsia_Bookingreg.stanytsia_day)  # повернення до дати
        await message.answer("Введіть день у форматі РРРР-ММ-ДД. Наприклад: 2024-05-20")
    else:
        response = await add_calendar_event(data, start_datetime.isoformat(), end_datetime.isoformat(), STANYTSIA_TEAMUP_CALENDAR_ID, STANYTSIA_TEAMUP_API_KEY, "stanytsia")
        if 'event' in response:
            db = db_booking.Booking_DataBase("db_plast.db")
            db.add_book_reg(
                user_id=message.from_user.id,
                user_name=message.from_user.first_name, 
                user_surname=message.from_user.last_name,
                user_domivka="станиця",
                user_room=data["stanytsia_number_of_room"],      
                user_date=data["stanytsia_day"],
                user_start_time=data["stanytsia_start_time"],
                user_end_time=data["stanytsia_end_time"],
                code_of_booking=response['event'].get('id', 'no_code') 
            )
            await message.answer("Ваше бронювання заповнено")
        else:
            await message.answer("Сталася помилка при додаванні події. Спробуйте ще раз або зверніться до офісу Пласту @lvivplastoffice.")
        await state.clear()

    # Debugging print statements
    print(data["stanytsia_booking_name"])
    print(data["stanytsia_number_of_room"])
    print(data["stanytsia_start_time"])
    print(data["stanytsia_end_time"])

