import asyncio
import requests
import re
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import bots
import keyboards
from datetime import datetime
import pytz
from calendars import VYNNYKY_TEAMUP_API_KEY, VYNNYKY_TEAMUP_CALENDAR_ID
from . import db_booking
from .booking_menu import fetch_calendar_events, add_calendar_event, check_event_conflicts
from handlers.start_menu import user_db
from handlers.booking_handler.botton_kb import create_cancel_button
from calendars import get_subcalendars

router = Router()
bot = Bot(bots.main_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
approved = []


class vynnyky_Bookingreg(StatesGroup):
    vynnyky_number_of_room = State()
    vynnyky_day = State()
    vynnyky_start_time = State()
    vynnyky_end_time = State()


@router.callback_query(F.data == "vynnyky")
async def bookstanytsia(callback: types.CallbackQuery):
    if len(approved) < 1:
        await callback.message.edit_reply_markup()
        await callback.message.edit_text(
            "Чудовий вибір! Перш за все, давай ознайомимось із <a "
            "href='https://docs.google.com/document/d/1t2F3z0Js5R31bl_9qfp_OolrA1D17S-S4y-aXicusf0/edit?usp=sharing'>правилами</a>. "
            "Знаю, читати їх буває "
            "нудно, але часто завдяки правилам можна дізнатись надзвичайно важливу інформацію, а також уникнути зайвих "
            "непорозумінь. Тож не лінуйся, прочитай — підніми настрій нашому офіс-менеджеру 👷🏻‍♂️ \n \n❗️Натискаючи "
            "\"Погоджуюсь із правилами\", ти підтверджуєш своє ознайомлення і обіцяєш чемно їх виконувати 🫡",
            reply_markup=keyboards.approovancebuilder_v,
            parse_mode=ParseMode.HTML)
    else:
        await callback.message.edit_reply_markup()
        await callback.message.edit_text(
           "Перед тим, як натиснути <b>\"Зареєструвати бронювання\"</b>, переглянь <b>календар бронювань</b> та перевір, чи точно вільне приміщення в потрібний тобі час 📅", 
            reply_markup=keyboards.vynnykykb, parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "approoved_v")
@router.callback_query(F.data == "RegistrateBookingVynnyky")
async def bookvynnyky(callback: types.CallbackQuery):
    approved.append(1)
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(
        """🏠 Для того, аби забронювати Вишкільний центр ім. Петра Франка у Винниках напиши нам у телеграм @lvivplastoffice або ж зателефонуй за номером +380951215011

🚪 У своєму повідомленні вкажи кількість осіб, які будуть присутні на заході та вибери зони, які вам будуть потрібні (у центрі є два поверхи: великий зал із проектором, а також кухня на першому пверсі та кілька окремих кімнат на другому)

📆 Обов'язково напиши часовий проміжок бронювання (дата і час), а також вкажи, чи є необхідність ночівлі""", reply_markup=keyboards.vynnykybooking_kb, parse_mode=ParseMode.HTML)


# @router.callback_query(F.data == "RegistrateBookingVynnyky")
# async def reg_vynnyky_two(callback_query: CallbackQuery, state: FSMContext):
#     await callback_query.message.edit_reply_markup()
#     await state.set_state(vynnyky_Bookingreg.vynnyky_number_of_room)
#     await callback_query.message.edit_text("🚪Обери номер кімнати:", reply_markup=keyboards.vynnyky_rooms_builder.as_markup())


# @router.callback_query(vynnyky_Bookingreg.vynnyky_number_of_room)
# async def reg_vynnyky_three(callback: CallbackQuery, state: FSMContext):
#     await callback.message.edit_reply_markup()
#     await callback.message.delete()
#     await state.update_data(vynnyky_number_of_room=callback.data)
#     await state.set_state(vynnyky_Bookingreg.vynnyky_day)
#     await callback.message.answer("Введи день у форматі ДД-ММ-РРРР. \n 📆Наприклад: 20-05-2024")


# @router.message(vynnyky_Bookingreg.vynnyky_day)
# async def reg_vynnyky_four(message: Message, state: FSMContext):
#     date_pattern = r"^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-\d{4}$"

#     if not re.match(date_pattern, message.text):
#         await message.answer(
#             "Неправильний формат дати. Будь ласка, введи день у форматі ДД-ММ-РРРР. \n 📆Наприклад: 20-05-2024")
#         return

#     day, month, year = message.text.split('-')
#     formatted_date = f"{year}-{month}-{day}"

#     await state.update_data(vynnyky_day=formatted_date)

#     await state.set_state(vynnyky_Bookingreg.vynnyky_start_time)
#     await message.answer("Введи час початку у форматі ГГ:ХХ. \n ⏰Наприклад 15:00")


# @router.message(vynnyky_Bookingreg.vynnyky_start_time)
# async def reg_vynnyky_five(message: Message, state: FSMContext):
#     time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
#     if not re.match(time_pattern, message.text):
#         await message.answer("Неправильний формат часу. Будь ласка, введи час у форматі ГГ:ХХ. \n ⏰Наприклад 15:00")
#         return
#     await state.update_data(vynnyky_start_time=message.text)
#     await state.set_state(vynnyky_Bookingreg.vynnyky_end_time)
#     await message.answer("Введи час закінчення у форматі ГГ:ХХ. \n ⏰Наприклад 16:00")


# @router.message(vynnyky_Bookingreg.vynnyky_end_time)
# async def reg_vynnyky_six(message: Message, state: FSMContext):
#     time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
#     if not re.match(time_pattern, message.text):
#         await message.answer("Неправильний формат часу. Будь ласка, введи час у форматі ГГ:ХХ. \n ⏰Наприклад 16:00")
#         return
#     await state.update_data(vynnyky_end_time=message.text)
#     data = await state.get_data()

#     vynnyky_room_mapping = get_subcalendars(VYNNYKY_TEAMUP_CALENDAR_ID, VYNNYKY_TEAMUP_API_KEY)
#     if data["vynnyky_number_of_room"] in vynnyky_room_mapping:
#         room = data["vynnyky_number_of_room"]
#         data["vynnyky_number_of_room"] = vynnyky_room_mapping[data["vynnyky_number_of_room"]]
#     else:
#         await message.answer("Виникла проблема при виборі кімнати. Зареєструй бронювання ще раз.")
#         await state.set_state(vynnyky_Bookingreg.vynnyky_number_of_room)
#         await bot.send_message(chat_id=message.from_user.id, text="Введи назву події")
#         return

#     local_tz = pytz.timezone("Europe/Kiev")
#     start_datetime = local_tz.localize(
#         datetime.strptime(f'{data["vynnyky_day"]} {data["vynnyky_start_time"]}', '%Y-%m-%d %H:%M')).astimezone(pytz.utc)
#     end_datetime = local_tz.localize(
#         datetime.strptime(f'{data["vynnyky_day"]} {data["vynnyky_end_time"]}', '%Y-%m-%d %H:%M')).astimezone(pytz.utc)

#     print(
#         f"Checking conflicts for room {data['vynnyky_number_of_room']} from {start_datetime.isoformat()} to {end_datetime.isoformat()}")
#     if await check_event_conflicts(data["vynnyky_number_of_room"], start_datetime.isoformat(), end_datetime.isoformat(),
#                                    VYNNYKY_TEAMUP_CALENDAR_ID, VYNNYKY_TEAMUP_API_KEY):
#         await message.answer("На цей час у вибраній кімнаті вже є подія. Вибери інший час.")
#         await state.set_state(vynnyky_Bookingreg.vynnyky_day)  # повернення до дати
#         await message.answer("Введи день у форматі ДД-ММ-РРРР. \n 📆Наприклад: 20-05-2024")
#     else:
#         response = await add_calendar_event(data, start_datetime.isoformat(), end_datetime.isoformat(),
#                                             VYNNYKY_TEAMUP_CALENDAR_ID, VYNNYKY_TEAMUP_API_KEY, "vynnyky", message)
#         if 'event' in response:
#             user_db_obj = user_db.DataBase("db_plast.db").get_user(message.from_user.id)
#             db = db_booking.BookingDataBase("db_plast.db")
#             db.add_book_reg(user_id=message.from_user.id, user_name=user_db_obj['user_name'],
#                             user_surname=user_db_obj['user_surname'], user_domivka="Винники", user_room=room,
#                             user_date=data["vynnyky_day"], user_start_time=data["vynnyky_start_time"],
#                             user_end_time=data["vynnyky_end_time"],
#                             code_of_booking=response['event'].get('id', 'no_code'))
#             await message.answer(
#                 'Твоє бронювання бронювання заповнено.🥳 Ти можеш переглянути його у <i><a href="https://teamup.com/kstbv5srw3gter52zv">календарі</a></i>. Якщо виникли проблеми, то звертайся до офісу пласту @lvivplastoffice',
#                 parse_mode=ParseMode.HTML,
#                 reply_markup=keyboards.mainkb)
#             if user_db_obj['user_nickname'] is None:
#                 nickname_text = ''
#             else:
#                 nickname_text = f'Нікнейм @{user_db_obj['user_nickname']}'

#             await bot.send_message(chat_id=-1002421947656,
#                                    text=f'''Бронювання #В{response['event'].get('id', 'no_code')}
# Ім'я: {user_db_obj['user_name']}
# Прізвище: {user_db_obj['user_surname']}
# Номер телефону: {user_db_obj['user_phone']}
# {nickname_text}
# Домівка: Винники
# Кімната: {room}
# День: {data["vynnyky_day"]}
# Час: {data["vynnyky_start_time"]} - {data["vynnyky_end_time"]}
# ''', reply_markup=create_cancel_button(user_db_obj['user_id'], response['event'].get('id', 'no_code'), 'В'))
#         else:
#             await message.answer(
#                 "Сталася помилка при додаванні події.☹️ Спробуйте ще раз або зверніться до офісу Пласту @lvivplastoffice.")
#         await state.clear()
