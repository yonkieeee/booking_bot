import requests
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from handlers.booking_handler.db_booking import Booking_DataBase
from handlers.booking_handler import botton_kb
from handlers.start_menu import bools
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import keyboards
import bots
import calendars

router = Router()
db = Booking_DataBase("db_plast.db")
bot = Bot(bots.main_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message(F.text == 'Мої бронювання✍🏻')
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
            cancel = botton_kb.create_cancel_button(message.from_user.id, booking['code'],
                                                    str(booking['domivka'])[0])
            await message.answer(
                f"""Бронювання #{booking['domivka'][0]}{booking['code']}
Назва: {booking['name_of_booking']}
Домівка: {booking['domivka']}
Кімната: {booking['room']}
Дата: {booking['date']}
Час: {booking['start_time']} - {booking['end_time']}""", reply_markup=cancel)


@router.callback_query(lambda c: c.data.startswith('cancel_'))
async def delete_booking(callback_query: CallbackQuery):
    booking_info = callback_query.data[7:].split('_')
    booking_code, user_id, domivka = booking_info
    print(callback_query.data)
    print(booking_info)
    
    db.delete_booking(user_id, booking_code)
    

    print(f"Код бронювання: {booking_code}, Домівка: {domivka}") 
    if (domivka == "Cтаниця"):
        await delete_teamup_event(calendars.STANYTSIA_TEAMUP_CALENDAR_ID, booking_code, calendars.STANYTSIA_TEAMUP_API_KEY)
    elif (domivka == "Винники"):
        await delete_teamup_event(calendars.VYNNYKY_TEAMUP_CALENDAR_ID, booking_code, calendars.VYNNYKY_TEAMUP_API_KEY)

    db.delete_booking(user_id, booking_code)
    await callback_query.message.delete()
    if callback_query.message.chat.id == -1002421947656:
        await bot.send_message(chat_id=-1002421947656,
                               text=f'''Скасовано бронювання #{domivka}{booking_code}''')
        await bot.send_message(chat_id=user_id, text=f'''Твоє бронювання #{domivka}{booking_code} скасували''' )
    else:
        await callback_query.message.answer(f"Бронювання #{domivka}{booking_code} успішно скасовано.")
        db.delete_booking(user_id, booking_code)
        await bot.send_message(chat_id=-1002421947656,
                               text=f'''Скасовано бронювання #{domivka}{booking_code}''')


async def delete_teamup_event(calendar_id, event_id, api_key):
    url = f"https://api.teamup.com/{calendar_id}/events/{event_id}"
    headers = {
        "Teamup-Token": api_key,
    }

    print(f"Видалення події: {url}")  

    response = requests.delete(url, headers=headers)

    print(f"Статус відповіді: {response.status_code}, Тіло відповіді: {response.text}") 
    
@router.message(F.text.lower() == 'повернутись до меню')
async def return_to_main(message: types.Message):
    await message.answer("Обери розділ", reply_markup=keyboards.mainkb)
