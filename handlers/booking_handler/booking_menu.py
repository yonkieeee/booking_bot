import asyncio
import requests
import re
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import bots
import keyboards
from datetime import datetime
import pytz
from calendars import STANYTSIA_TEAMUP_API_KEY, STANYTSIA_TEAMUP_CALENDAR_ID
from . import db_booking
from handlers.start_menu import user_db

router = Router()
bot = Bot(bots.main_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message(F.text.lower() == "бронювання")
async def booking(message: types.Message):
    await message.reply(
        "Чудовий вибір! Перш за все, давай ознайомимось із правилами (https://drive.google.com/file/d/1GIXwD2PadsRAc2wC5RRb4M4bMLBE7jyf/view?usp=sharing). Знаю, читати їх буває нудно, але часто завдяки правилам можна дізнатись надзвичайно важливу інформацію, а також уникнути зайвих непорозумінь. Тож не лінуйся, прочитай — підніми настрій нашому офіс-менеджеру 👷🏻‍♂️❗️Натискаючи \"Погоджуюсь із правилами\", ти підтверджуєш своє ознайомлення і обіцяєш чемно їх виконувати 🫡",
        reply_markup=keyboards.approovancebuilder.as_markup(),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "approoved")
async def chooselocation(callback: types.CallbackQuery):
    await callback.message.answer("🤝Дякую за співпрацю! Тепер обери приміщення:", reply_markup=keyboards.bookingk)


@router.callback_query(F.data == "non_approoved")
async def chooselocation(callback: types.CallbackQuery):
    await callback.message.answer("Тоді обери інший пункт меню", reply_markup=keyboards.mainkb)


async def fetch_calendar_events(subcalendar_id, start_dt, end_dt, TEAMUP_CALENDAR_ID, TEAMUP_API_KEY):
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_ID}/events"
    params = {
        "startDate": start_dt,
        "endDate": end_dt,
        "subcalendarId[]": [subcalendar_id]
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


async def check_event_conflicts(subcalendar_id, new_start, new_end, TEAMUP_CALENDAR_ID, TEAMUP_API_KEY):
    print(f"Fetching existing events for room {subcalendar_id} from {new_start} to {new_end}")

    existing_events = await fetch_calendar_events(subcalendar_id, new_start, new_end, TEAMUP_CALENDAR_ID,
                                                  TEAMUP_API_KEY)

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


async def add_calendar_event(data, start_dt, end_dt, TEAMUP_CALENDAR_ID, TEAMUP_API_KEY, domivka, message):
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_ID}/events"
    headers = {"Teamup-Token": TEAMUP_API_KEY, "Content-Type": "application/json"}
    user_db_obj = user_db.DataBase("db_plast.db").get_user(message.from_user.id)

    event_data = {
        "subcalendar_ids": [data[domivka + "_" + "number_of_room"]],
        "title": data[domivka + "_" + "booking_name"],
        "start_dt": start_dt,
        "end_dt": end_dt,
        "who": user_db_obj['user_name'] + " " + user_db_obj['user_surname']
    }
    print("Sending Event Data:", event_data)  # Debugging print to verify event data before sending
    response = requests.post(url, headers=headers, json=event_data)
    print("Add event response:", response.status_code, response.text)  # Debugging print to verify response
    return response.json()