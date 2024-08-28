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
import aiohttp
import sqlite3
BOT_TOKEN = "7155709020:AAHakRNl6kPuLlutrw9OF_DjyG4aEA68BHA"
TEAMUP_CALENDAR_ID = "ksmr4o4huehb9n9sph"
TEAMUP_API_KEY = "3483fc717a58e4453a2742b1d98c34e6eba12eed3a8ec74f3997842e3366702a"

router = Router()
db = DataBase("db_plast.db")
bot = Bot("7155709020:AAHakRNl6kPuLlutrw9OF_DjyG4aEA68BHA")
disp = Dispatcher(bot)

class Booking_DataBase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT,
                room TEXT,
                date TEXT,
                start_time TEXT,
                end_time TEXT,
                code TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def get_user_bookings(self, user_id):
        self.cursor.execute('''
            SELECT * FROM booking
            WHERE user_id = ?
            AND date >= date('now')
            AND (date > date('now') OR (date = date('now') AND end_time > time('now')))
        ''', (user_id,))
        return self.cursor.fetchall()

    def delete_booking(self, user_id, booking_code):
        self.cursor.execute('''
            DELETE FROM booking
            WHERE user_id = ? AND code = ?
        ''', (user_id, booking_code))
        self.conn.commit()

    def close(self):
        self.conn.close()

class Bookingreg(StatesGroup):
    booking_name = State()
    number_of_room = State()
    day = State()
    start_time = State()
    end_time = State()
    cancel_booking_code = State()

@router.message(Command())
async def start(message: types.Message):
    await message.reply("Вітаю! Використовуйте команди для управління бронюваннями.")

@router.message(Text(text="перегляд бронювань", ignore_case=True))
async def view_bookings(message: types.Message):
    db = Booking_DataBase("db_plast.db")  
    active_bookings = db.get_user_bookings(message.from_user.id)
    if not active_bookings:
        await message.reply("Немає активних бронювань.")
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)
        for booking in active_bookings:
            button = InlineKeyboardButton(
                text=f"ID: {booking[0]}, Назва: {booking[2]}, Кімната: {booking[3]}, Дата: {booking[4]}",
                callback_data=f"cancel_{booking[7]}"
            )
            keyboard.add(button)
        await message.reply("Виберіть бронювання для скасування:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data and c.data.startswith('cancel_'))
async def handle_cancel_booking(callback_query: types.CallbackQuery):
    booking_code = callback_query.data.split('_', 1)[1]
    user_id = callback_query.from_user.id

    db = Booking_DataBase("db_plast.db") 
    booking = db.get_user_bookings(user_id)
    if any(b[7] == booking_code for b in booking):
        db.delete_booking(user_id, booking_code)
        await remove_calendar_event(booking_code)
        await callback_query.message.reply("Бронювання скасовано.")
    else:
        await callback_query.message.reply("Не знайдено бронювання з таким кодом.")

async def remove_calendar_event(booking_code):
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_ID}/events/{booking_code}"
    headers = {"Teamup-Token": TEAMUP_API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                print("Подію видалено.")
            else:
                print("Помилка запиту:", response.status, await response.text())


