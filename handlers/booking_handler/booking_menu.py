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
from calendars import TEAMUP_API_KEY, TEAMUP_CALENDAR_ID
import db_booking

router = Router()

bot = Bot(bots.main_bot)


class Bookingreg(StatesGroup):
    booking_name = State()
    number_of_room = State()
    day = State()
    start_time = State()
    end_time = State()

@router.message(F.text.lower() == "бронювання")
async def booking(message: types.Message):
    await message.reply(
        'В цьому розділі ви можете забронювати приміщення. Але Перш ніж це зробити ознайомтесь з <a href="https://drive.google.com/file/d/1GIXwD2PadsRAc2wC5RRb4M4bMLBE7jyf/view?usp=sharing"> правилами</a>.        \n'
        "Натискаючи кнопку 'так, підтверджую, ти погоджуєшся з усіма праилами та забов'язуєшся їх виконувати",
        reply_markup=keyboards.approovancebuilder.as_markup()
    )

@router.callback_query(F.data == "approoved")
async def chooselocation(callback: types.CallbackQuery):
    await callback.message.answer("Обери приміщення", reply_markup=keyboards.bookingk)

@router.callback_query(F.data == "non_approoved")
async def chooselocation(callback: types.CallbackQuery):
    await callback.message.answer("Тоді обери інший пункт меню", reply_markup=keyboards.mainkb)

@router.callback_query(F.data == "stanytsia")
async def bookstanytsia(callback: types.CallbackQuery):
    await callback.message.answer("Перед натисканням на кнопку 'Реєстрація бронювання' переглянь графік", reply_markup=keyboards.stanytsiakb)

@router.callback_query(F.data == "RegistrateBookingStanytsia")
async def reg_stanytsia_one(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Bookingreg.booking_name)
    await bot.send_message(chat_id=callback.from_user.id, text="Введіть назву події")

@router.message(Bookingreg.booking_name)
async def reg_stanytsia_two(message: Message, state: FSMContext):
    await state.update_data(booking_name=message.text)
    await state.set_state(Bookingreg.number_of_room)
    await message.answer("Оберіть номер кімнати", reply_markup=keyboards.room_inline)

@router.callback_query(Bookingreg.number_of_room)
async def reg_stanytsia_three(callback: CallbackQuery, state: FSMContext):
    await state.update_data(number_of_room=callback.data)
    await state.set_state(Bookingreg.day)
    await callback.message.answer("Введіть день у форматі РРРР-ММ-ДД. Наприклад: 2024-05-20")

@router.message(Bookingreg.day)
async def reg_stanytsia_four(message: Message, state: FSMContext):
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(date_pattern, message.text):
        await message.answer("Неправильний формат дати. Будь ласка, введіть день у форматі РРРР-ММ-ДД. Наприклад: 2024-05-20")
        return
    await state.update_data(day=message.text)
    await state.set_state(Bookingreg.start_time)
    await message.answer("Введіть час початку у форматі ГГ:ХХ. Наприклад 15:00")

@router.message(Bookingreg.start_time)
async def reg_stanytsia_five(message: Message, state: FSMContext):
    time_pattern = r"^\d{2}:\d{2}$"
    if not re.match(time_pattern, message.text):
        await message.answer("Неправильний формат часу. Будь ласка, введіть час у форматі ГГ:ХХ. Наприклад 15:00")
        return
    await state.update_data(start_time=message.text)
    await state.set_state(Bookingreg.end_time)
    await message.answer("Введіть час закінчення у форматі ГГ:ХХ. Наприклад 16:00")


@router.message(Bookingreg.end_time)
async def reg_stanytsia_six(message: Message, state: FSMContext):
    time_pattern = r"^\d{2}:\d{2}$"
    if not re.match(time_pattern, message.text):
        await message.answer("Неправильний формат часу. Будь ласка, введіть час у форматі ГГ:ХХ. Наприклад 16:00")
        return
    await state.update_data(end_time=message.text)
    data = await state.get_data()
    
    room_mapping = {"303": 13281316, "203": 13281315}
    if data["number_of_room"] in room_mapping:
        data["number_of_room"] = room_mapping[data["number_of_room"]]
    else:
        await message.answer("Ви ввели неправильний номер кімнати. Зареєструйте бронювання ще раз.")
        await state.set_state(Bookingreg.booking_name)
        await bot.send_message(chat_id=message.from_user.id, text="Введіть назву події")
        return

    local_tz = pytz.timezone("Europe/Kiev")
    start_datetime = local_tz.localize(datetime.strptime(f'{data["day"]} {data["start_time"]}', '%Y-%m-%d %H:%M')).astimezone(pytz.utc)
    end_datetime = local_tz.localize(datetime.strptime(f'{data["day"]} {data["end_time"]}', '%Y-%m-%d %H:%M')).astimezone(pytz.utc)

    print(f"Checking conflicts for room {data['number_of_room']} from {start_datetime.isoformat()} to {end_datetime.isoformat()}")
    if await check_event_conflicts(data["number_of_room"], start_datetime.isoformat(), end_datetime.isoformat()):
        await message.answer("На цей час у вибраній кімнаті вже є подія. Виберіть інший час.")
        await state.set_state(Bookingreg.day)  # повернення до дати
        await message.answer("Введіть день у форматі РРРР-ММ-ДД. Наприклад: 2024-05-20")
    else:
        response = await add_calendar_event(data, start_datetime.isoformat(), end_datetime.isoformat())
        if 'event' in response:
            db = db_booking.Booking_DataBase("db_plast.db")
            db.add_book_reg(
                user_id=message.from_user.id,
                user_name=message.from_user.first_name, 
                user_surname=message.from_user.last_name,  
                user_domivka="станиця",
                user_room=data["number_of_room"],      
                user_date=data["day"],
                user_start_time=data["start_time"],
                user_end_time=data["end_time"],
                code_of_booking=response['event'].get('id', 'no_code') 
            )
            await message.answer("Ваше бронювання заповнено")
        else:
            await message.answer("Сталася помилка при додаванні події. Спробуйте ще раз або зверніться до офісу Пласту @lvivplastoffice.")
        await state.clear()

    # Debugging print statements
    print(data["booking_name"])
    print(data["number_of_room"])
    print(data["start_time"])
    print(data["end_time"])


async def fetch_calendar_events(subcalendar_id, start_dt, end_dt):
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_ID}/events"
    params = {
        "startDate": start_dt,
        "endDate": end_dt,
        "subcalendarId[]": [subcalendar_id]  # Make sure this is an array
    }
    headers = {"Teamup-Token": TEAMUP_API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        events = response.json().get("events", [])
        print(f"Fetched events: {events}")
        return events
    else:
        print("Failed to fetch events:", response.status_code, response.text)
        return []


async def check_event_conflicts(subcalendar_id, new_start, new_end):
    print(f"Fetching existing events for room {subcalendar_id} from {new_start} to {new_end}")
    
    existing_events = await fetch_calendar_events(subcalendar_id, new_start, new_end)
    
    # Convert new_start and new_end to datetime objects
    new_start_dt = datetime.fromisoformat(new_start)
    new_end_dt = datetime.fromisoformat(new_end)
    
    for event in existing_events:
        event_start = datetime.fromisoformat(event['start_dt'])
        event_end = datetime.fromisoformat(event['end_dt'])
        
        print(f"Checking event {event['id']} from {event_start} to {event_end}")
        if (event_start < new_end_dt) and (event_end > new_start_dt):
            print("Conflict found!")
            return True  # Conflict found
    
    print("No conflict found.")
    return False  # No conflict



async def add_calendar_event(data, start_dt, end_dt):
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_ID}/events"
    headers = {"Teamup-Token": TEAMUP_API_KEY, "Content-Type": "application/json"}
    event_data = {
        "subcalendar_ids": [data["number_of_room"]],
        "title": data["booking_name"],
        "start_dt": start_dt,
        "end_dt": end_dt,
    }
    print("Sending Event Data:", event_data)  # Debugging print to verify event data before sending
    response = requests.post(url, headers=headers, json=event_data)
    print("Add event response:", response.status_code, response.text)  # Debugging print to verify response
    return response.json()
