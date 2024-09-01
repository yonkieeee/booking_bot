import requests
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from handlers.booking_handler.db_booking import Booking_DataBase
from handlers.booking_handler import botton_kb
from datetime import datetime
import keyboards
import calendars

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
    
    domivka = db.get_domivka(booking_code)

    print(f"Код бронювання: {booking_code}, Домівка: {domivka}")  # Додаємо відладкове повідомлення
    if (domivka == "Cтаниця"):
        await delete_teamup_event(calendars.STANYTSIA_TEAMUP_CALENDAR_ID, booking_code, calendars.STANYTSIA_TEAMUP_API_KEY)
    elif (domivka == "Винники"):
        await delete_teamup_event(calendars.VYNNYKY_TEAMUP_CALENDAR_ID, booking_code, calendars.VYNNYKY_TEAMUP_API_KEY)
    
    db.delete_booking(user_id, booking_code)
    await callback_query.message.delete()
    await callback_query.message.answer(f"Бронювання №{booking_code} успішно видалено.")
    
async def delete_teamup_event(calendar_id, event_id, api_key):
    url = f"https://api.teamup.com/{calendar_id}/events/{event_id}"
    headers = {
        "Teamup-Token": api_key,
    }

    print(f"Видалення події: {url}")  
    
    response = requests.delete(url, headers=headers)
    
    print(f"Статус відповіді: {response.status_code}, Тіло відповіді: {response.text}") 

    if response.status_code == 204:
        return True
    elif response.status_code == 404:
        return False
    else:
        return False

@router.message(F.text.lower() == 'повернутись до меню')
async def return_to_main(message: types.Message):
    await message.answer("Обери розділ", reply_markup=keyboards.mainkb)
