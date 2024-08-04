
import asyncio
import requests
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import bots
import keyboards

router = Router()

bot = Bot(bots.main_bot)
TEAMUP_CALENDAR_ID = "ksmr4o4huehb9n9sph"
TEAMUP_API_KEY = "3483fc717a58e4453a2742b1d98c34e6eba12eed3a8ec74f3997842e3366702a"

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

@router.callback_query(F.data == "RegistrateBookinStanytsia")
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

@router.message(Bookingreg.end_time)
async def reg_stanytsia_six(message: Message, state: FSMContext):
    await state.update_data(end_time=message.text)
    data = await state.get_data()
    if data["number_of_room"] == "303":
        data["number_of_room"] = 13281316
    elif data["number_of_room"] == "203":
        data["number_of_room"] = 13281315
    else:
        await message.answer("Ви ввели неправильний номер кімнати. Зареєструйте бронювання ще раз.")
        await state.set_state(Bookingreg.booking_name)
        await bot.send_message(chat_id=message.from_user.id, text="Введіть назву події")
        return

    start_datetime = f'{data["day"]}T{data["start_time"]}:00Z'
    end_datetime = f'{data["day"]}T{data["end_time"]}:00Z'

    if await check_event_conflicts(start_datetime, end_datetime):
        await message.answer("There is already an event at this time. Please choose a different time.")
        await state.clear()
    else:
        response = await add_calendar_event(data)
        if 'event' in response:
            await message.answer("Ваше бронювання заповнено")
        else:
            await message.answer("Сталася помилка при додаванні події. Спробуйте ще раз.")
        await state.clear()

    # Debugging print statements
    print(data["booking_name"])
    print(data["number_of_room"])
    print(data["start_time"])
    print(data["end_time"])

# Your existing functions
async def fetch_calendar_events(start_dt, end_dt):
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_ID}/events"
    params = {
        "startDate": start_dt,
        "endDate": end_dt
    }
    headers = {"Teamup-Token": TEAMUP_API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("events", [])
    else:
        print("Failed to fetch events:", response.status_code, response.text)
        return []

async def check_event_conflicts(new_start, new_end):
    existing_events = await fetch_calendar_events(new_start, new_end)
    for event in existing_events:
        event_start = event['start_dt']
        event_end = event['end_dt']
        if (event_start < new_end) and (event_end > new_start):
            return True  # Conflict found
    return False  # No conflict

async def add_calendar_event(data):
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_ID}/events"
    headers = {"Teamup-Token": TEAMUP_API_KEY, "Content-Type": "application/json"}
    event_data = {
        "subcalendar_ids": [data["number_of_room"]],
        "title": data["booking_name"],
        "start_dt": f'{data["day"]}T{data["start_time"]}:00Z',
        "end_dt": f'{data["day"]}T{data["end_time"]}:00Z',
    }
    print("Sending Event Data:", event_data)  # Debugging print to verify event data before sending
    response = requests.post(url, headers=headers, json=event_data)
    print("Add event response:", response.status_code, response.text)
    return response.json()
