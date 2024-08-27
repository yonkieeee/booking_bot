from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from handlers.start_menu.user_db import DataBase
from handlers.start_menu import bools
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from handlers.start_menu import start_keyboard as kb
import keyboards
import sqlite3
BOT_TOKEN = "7155709020:AAHakRNl6kPuLlutrw9OF_DjyG4aEA68BHA"
TEAMUP_CALENDAR_ID = "ksmr4o4huehb9n9sph"
TEAMUP_API_KEY = "3483fc717a58e4453a2742b1d98c34e6eba12eed3a8ec74f3997842e3366702a"

router = Router()
db = DataBase("db_plast.db")
bot = Bot("7155709020:AAHakRNl6kPuLlutrw9OF_DjyG4aEA68BHA")
disp = Dispatcher(bot)

class Bookingreg(StatesGroup):
    booking_name = State()
    number_of_room = State()
    day = State()
    start_time = State()
    end_time = State()

@router.message(F.text.lower() == "перегляд бронювань")
async def view_bookings(message: types.Message):
    db = Booking_DataBase("db_plast.db")  
    active_bookings = db.get_active_bookings()
    if not active_bookings:
        await message.reply("Немає активних бронювань.")
    else:
        response = "Актуальні бронювання:\n"
        for booking in active_bookings:
            response += f"ID: {booking.id}, Назва: {booking.name}, Кімната: {booking.room}, Дата: {booking.date}, Початок: {booking.start_time}, Кінець: {booking.end_time}\n"
        await message.reply(response)

@router.message(F.text.lower() == "скасувати бронювання")
async def cancel_booking(message: types.Message):
    await message.reply("Введіть код бронювання для скасування:")

@router.message()
async def handle_cancel_booking(message: types.Message):
    user_id = message.from_user.id
    booking_code = message.text

    db = Booking_DataBase("db_plast.db") 
    db.delete_booking(user_id, booking_code)

    await remove_calendar_event(booking_code)

    await message.reply("Бронювання скасовано.")

async def remove_calendar_event(booking_code):
    db = Booking_DataBase("db_plast.db")
    booking = db.session.query(Book_Reg).filter_by(code=booking_code).first()
    
    if booking:
        url = f"https://api.teamup.com/{TEAMUP_CALENDAR_ID}/events/{booking_code}"
        headers = {"Teamup-Token": TEAMUP_API_KEY}
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    print("Подію видалено.")
                else:
                    print("Помилка запиту:", response.status, await response.text())
    else:
        print("Не знайдено бронювання.")
