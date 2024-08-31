from aiogram import Router, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from handlers.booking_handler.db_booking import Booking_DataBase
from handlers.booking_handler import botton_kb
from handlers.start_menu import bools
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import keyboards

router = Router()
db = Booking_DataBase("db_plast.db")


@router.message(F.text.lower() == 'глянути всі бронювання')
async def view_bookings(message: types.Message):
    active_bookings = db.get_all_data(message.from_user.id)
    current_time = datetime.now().replace(second=0, microsecond=0)
    print(current_time)
    valid_bookings = []

    for booking in active_bookings:
        date = booking['date'] + " " + booking['end_time'] + ":00"
        print(date)
        end_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        if end_time > current_time:
            valid_bookings.append(booking)
        else:
            db.delete_booking(message.from_user.id, booking['code'])

    if not valid_bookings:
        await message.answer("Не має активних бронювань")
    else:
        await message.answer("Актуальні бронювання", reply_markup=botton_kb.return_kb)
        for booking in valid_bookings:
            count = 0
            cancel = botton_kb.create_cancel_button(booking['code'])
            await message.answer(
                f"""Бронювання №: {booking['code']}

Домівка: {booking['domivka']}
Кімната: {booking['room']}
Дата: {booking['date']}
Час: {booking['start_time']} - {booking['end_time']}""", reply_markup=cancel)


@router.callback_query(lambda c: c.data.startswith('cancel_'))
async def delete_booking(callback_query: CallbackQuery):
    booking_code = callback_query.data[7:]
    user_id = callback_query.from_user.id
    db.delete_booking(user_id, booking_code)

    await callback_query.message.delete()

    await callback_query.message.answer(f"Бронювання №{booking_code} успішно видалено.")


@router.message(F.text.lower() == 'повернутись до меню')
async def return_to_main(message: types.Message):
    await message.answer("Обери розділ", reply_markup=keyboards.mainkb)