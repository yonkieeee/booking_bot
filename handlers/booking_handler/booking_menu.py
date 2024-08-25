
import asyncio
from datetime import datetime, timedelta
import pytz
from pydantic import BaseModel
import requests
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.client.bot import DefaultBotProperties
import bots, keyboards
from . import db_booking
import calendars

router = Router()

bot = Bot(bots.main_bot, default=DefaultBotProperties(parse_mode="HTML"))


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
    await message.answer("Введіть номер кімнати")

@router.message(Bookingreg.number_of_room)
async def reg_stanytsia_three(message: Message, state: FSMContext):
    await state.update_data(number_of_room=message.text)
    await state.set_state(Bookingreg.day)
    await message.answer("Введіть день у форматі РРРР-ММ-ДД. Наприклад: 2024-05-20")

@router.message(Bookingreg.day)
async def reg_stanytsia_four(message: Message, state: FSMContext):
    await state.update_data(day=message.text)
    await state.set_state(Bookingreg.start_time)
    await message.answer("Введіть час початку у форматі ГГ:ХХ. Наприклад 15:00")

@router.message(Bookingreg.start_time)
async def reg_stanytsia_five(message: Message, state: FSMContext):
    await state.update_data(start_time=message.text)
    await state.set_state(Bookingreg.end_time)
    await message.answer("Введіть час закінчення у форматі ГГ:ХХ. Наприклад 16:00")

from datetime import datetime, timedelta
import pytz

# Приклад конвертації місцевого часу в UTC
def local_to_utc(local_dt_str, tz_str):
    local_tz = pytz.timezone(tz_str)
    local_dt = datetime.strptime(local_dt_str, '%Y-%m-%dT%H:%M:%S')
    local_dt = local_tz.localize(local_dt)
    utc_dt = local_dt.astimezone(pytz.UTC)
    return utc_dt.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

@router.message(Bookingreg.end_time)
async def reg_stanytsia_six(message: Message, state: FSMContext):
    await state.update_data(end_time=message.text)
    data = await state.get_data()

    if data["number_of_room"] == "303":
        stanytsia_subid = 13281316
    elif data["number_of_room"] == "203":
        stanytsia_subid = 13281315
    else:
        await message.answer("Ви ввели неправильний номер кімнати. Зареєструйте бронювання ще раз.")
        await state.set_state(Bookingreg.booking_name)
        await bot.send_message(chat_id=message.from_user.id, text="Введіть назву події")
        return

    # Конвертація часу з місцевого в UTC
    tz_str = 'Europe/Kiev'
    start_datetime = local_to_utc(f'{data["day"]}T{data["start_time"]}:00', tz_str)
    end_datetime = local_to_utc(f'{data["day"]}T{data["end_time"]}:00', tz_str)

    if await check_event_conflicts(start_datetime, end_datetime, calendars.TEAMUP_API_KEY):
        await message.answer("Це приміщення зайняте в цей час. Оберіть інший час.")
        await state.clear()
    else:
        response = await add_calendar_event(data, calendars.TEAMUP_API_KEY, calendars.TEAMUP_CALENDAR_ID, stanytsia_subid)
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
            await message.answer("Сталася помилка при додаванні події. Спробуйте ще раз.")
        await state.clear()

    # Debugging prints
    print(data["booking_name"])
    print(data["number_of_room"])
    print(data["start_time"])
    print(data["end_time"])

async def add_calendar_event(data, apikey, calendar_id, subid):
    url = f"https://api.teamup.com/{calendar_id}/events"
    headers = {"Teamup-Token": apikey, "Content-Type": "application/json"}
    event_data = {
        "subcalendar_ids": [subid],
        "title": data["booking_name"],
        "start_dt": f'{data["day"]}T{data["start_time"]}:00Z',
        "end_dt": f'{data["day"]}T{data["end_time"]}:00Z',
    }
    print("Sending Event Data:", event_data)  # Debugging print to verify event data before sending
    response = requests.post(url, headers=headers, json=event_data)
    print("Add event response:", response.status_code, response.text)
    return response.json()


async def fetch_calendar_events(start_dt, end_dt, apikey):
    apikey = "3483fc717a58e4453a2742b1d98c34e6eba12eed3a8ec74f3997842e3366702a"  # Перевірте правильність API-ключа
    url = f"https://api.teamup.com/ksmr4o4huehb9n9sph/events"
    
    # Дебаг-прінти для перевірки вхідних даних
    print("Fetching calendar events:")
    print(f"API Key: {apikey}")
    print(f"Start Date: {start_dt}")
    print(f"End Date: {end_dt}")
    
    params = {
        "startDate": start_dt,
        "endDate": end_dt
    }
    
    headers = {"Teamup-Token": apikey}
    
    try:
        # Відправляємо запит до API
        response = requests.get(url, headers=headers, params=params)
        
        # Дебаг-прінти для перевірки відповіді
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)
        
        if response.status_code == 200:
            events = response.json().get("events", [])
            print("Fetched Events:", events)  # Дебаг-прінт для перевірки подій
            return events
        else:
            print("Failed to fetch events:", response.status_code, response.text)
            return []
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


async def check_event_conflicts(new_start, new_end, apikey_):
    existing_events = await fetch_calendar_events(new_start, new_end, apikey_)
    for event in existing_events:
        event_start = event['start_dt']
        event_end = event['end_dt']
        if (event_start < new_end) and (event_end > new_start):
            return True  # Conflict found
    return False  # No conflict
