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
from calendars import STANYTSIA_TEAMUP_API_KEY, STANYTSIA_TEAMUP_CALENDAR_ID
from . import db_booking
from .booking_menu import fetch_calendar_events, add_calendar_event, check_event_conflicts
from handlers.start_menu import user_db
from handlers.booking_handler.botton_kb import create_cancel_button
from calendars import get_subcalendars

router = Router()
bot = Bot(bots.main_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
aprooved = []


class Stanytsia_Bookingreg(StatesGroup):
    stanytsia_number_of_room = State()
    stanytsia_day = State()
    stanytsia_start_time = State()
    stanytsia_end_time = State()


@router.callback_query(F.data == "stanytsia")
async def bookstanytsia(callback: types.CallbackQuery):
    if len(aprooved) < 1:
        await callback.message.edit_reply_markup()
        await callback.message.edit_text(
            "Чудовий вибір! Перш за все, давай ознайомимось із <a "
            "href='https://docs.google.com/document/d/1Wj5SvHRSfrgAw7oWq68VOVH5hjNeQOGsNqTaai1v-dg/edit?usp=drivesdk'>правилами</a>. "
            "Знаю, читати їх буває "
            "нудно, але часто завдяки правилам можна дізнатись надзвичайно важливу інформацію, а також уникнути зайвих "
            "непорозумінь. Тож не лінуйся, прочитай — підніми настрій нашому офіс-менеджеру 👷🏻‍♂️❗️Натискаючи "
            "\"Погоджуюсь із правилами\", ти підтверджуєш своє ознайомлення і обіцяєш чемно їх виконувати 🫡",
            reply_markup=keyboards.approovancebuilder,
            parse_mode=ParseMode.HTML)
    else:
        await callback.message.edit_reply_markup()
        await callback.message.edit_text(
            "Перед натисканням на кнопку <b>'Реєстрація бронювання'</b> переглянь <b>календар бронювань</b> для перевірки, чи є вільним приміщення в потрібний тобі час📅",
            reply_markup=keyboards.stanytsiakb, parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "approoved")
async def bookstanytsia(callback: types.CallbackQuery):
    aprooved.append(1)
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(
        "Перед натисканням на кнопку <b>'Реєстрація бронювання'</b> переглянь <b>календар бронювань</b> для перевірки, чи є вільним приміщення в потрібний тобі час📅",
        reply_markup=keyboards.stanytsiakb, parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "RegistrateBookingStanytsia")
async def reg_stanytsia_two(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    await state.set_state(Stanytsia_Bookingreg.stanytsia_number_of_room)
    await callback_query.message.edit_text("🚪Обери номер кімнати:", reply_markup=keyboards.stanytsia_rooms_builder.as_markup())


@router.callback_query(Stanytsia_Bookingreg.stanytsia_number_of_room)
async def reg_stanytsia_three(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.delete()
    await state.update_data(stanytsia_number_of_room=callback.data)
    await state.set_state(Stanytsia_Bookingreg.stanytsia_day)
    await callback.message.answer("Введи день у форматі ДД-ММ-РРРР. \n 📆Наприклад: 20-05-2024")


@router.message(Stanytsia_Bookingreg.stanytsia_day)
async def reg_stanytsia_four(message: Message, state: FSMContext):
    date_pattern = r"^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-\d{4}$"

    if not re.match(date_pattern, message.text):
        await message.answer(
            "Неправильний формат дати. Будь ласка, введи день у форматі ДД-ММ-РРРР. \n 📆Наприклад: 20-05-2024")
        return

    day, month, year = message.text.split('-')
    formatted_date = f"{year}-{month}-{day}"

    await state.update_data(stanytsia_day=formatted_date)
    await state.set_state(Stanytsia_Bookingreg.stanytsia_start_time)
    await message.answer("Введи час початку бронювання у форматі ГГ:ХХ \n ⏰Наприклад 15:00")


@router.message(Stanytsia_Bookingreg.stanytsia_start_time)
async def reg_stanytsia_five(message: Message, state: FSMContext):
    time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    if not re.match(time_pattern, message.text):
        await message.answer("Неправильний формат часу. Будь ласка, введи час у форматі ГГ:ХХ. \n ⏰Наприклад 15:00")
        return
    await state.update_data(stanytsia_start_time=message.text)
    await state.set_state(Stanytsia_Bookingreg.stanytsia_end_time)
    await message.answer("А тепер напиши час завершення \n ⏰Наприклад 16:00")


@router.message(Stanytsia_Bookingreg.stanytsia_end_time)
async def reg_stanytsia_six(message: Message, state: FSMContext):
    time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    if not re.match(time_pattern, message.text):
        await message.answer("Неправильний формат часу. Будь ласка, введи час у форматі ГГ:ХХ. \n ⏰Наприклад 16:00")
        return
    await state.update_data(stanytsia_end_time=message.text)
    data = await state.get_data()

    room_mapping = get_subcalendars(STANYTSIA_TEAMUP_CALENDAR_ID, STANYTSIA_TEAMUP_API_KEY)
    if data["stanytsia_number_of_room"] in room_mapping:
        room = data["stanytsia_number_of_room"]
        data["stanytsia_number_of_room"] = room_mapping[data["stanytsia_number_of_room"]]
    else:
        await message.answer("Виникла проблема при виборі кімнати. Зареєструй бронювання ще раз.")
        return

    local_tz = pytz.timezone("Europe/Kiev")
    start_datetime = local_tz.localize(
        datetime.strptime(f'{data["stanytsia_day"]} {data["stanytsia_start_time"]}', '%Y-%m-%d %H:%M')).astimezone(
        pytz.utc)
    end_datetime = local_tz.localize(
        datetime.strptime(f'{data["stanytsia_day"]} {data["stanytsia_end_time"]}', '%Y-%m-%d %H:%M')).astimezone(
        pytz.utc)

    print(
        f"Checking conflicts for room {data['stanytsia_number_of_room']} from {start_datetime.isoformat()} to {end_datetime.isoformat()}")
    if await check_event_conflicts(data["stanytsia_number_of_room"], start_datetime.isoformat(),
                                   end_datetime.isoformat(), STANYTSIA_TEAMUP_CALENDAR_ID, STANYTSIA_TEAMUP_API_KEY):
        await message.answer("На цей час у вибраній кімнаті вже є подія. Вибери інший час.")
        await state.set_state(Stanytsia_Bookingreg.stanytsia_day)  # повернення до дати
        await message.answer("Введи день у форматі РРРР-ММ-ДД. \n 📆Наприклад: 2024-05-20")
    else:
        response = await add_calendar_event(data, start_datetime.isoformat(), end_datetime.isoformat(),
                                            STANYTSIA_TEAMUP_CALENDAR_ID, STANYTSIA_TEAMUP_API_KEY, "stanytsia",
                                            message)
        if 'event' in response:
            user_db_obj = user_db.DataBase("db_plast.db").get_user(message.from_user.id)

            db = db_booking.BookingDataBase("db_plast.db")
            db.add_book_reg(user_id=message.from_user.id, user_name=user_db_obj['user_name'],
                            user_surname=user_db_obj['user_surname'], user_domivka="Cтаниця", user_room=room,
                            user_date=data["stanytsia_day"], user_start_time=data["stanytsia_start_time"],
                            user_end_time=data["stanytsia_end_time"],
                            code_of_booking=response['event'].get('id', 'no_code'))
            await message.answer(
                '🙌🏻 Неймовірно! Твоє бронювання бронювання підтверджено. Тепер його можна знайти у <i><a href="https://teamup.com/kstbv5srw3gter52zv">календарі</a></i>. \n\n❓Маєш додаткові запитання? Хочеш поділитись відгуком? @lvivplastoffice надасть зворотній зв\'язок 💬',
                parse_mode=ParseMode.HTML,
            reply_markup=keyboards.mainkb)
            await state.clear()

            if user_db_obj['user_nickname'] is None:
                nickname_text = ''
            else:
                nickname_text = f'Нікнейм @{user_db_obj['user_nickname']}'

            await bot.send_message(chat_id=-1002421947656,
                                   text=f'''Бронювання #С{response['event'].get('id', 'no_code')}
Ім'я: {user_db_obj['user_name']}
Прізвище: {user_db_obj['user_surname']}
Номер телефону: {user_db_obj['user_phone']}
{nickname_text}
Домівка: Станиця
Кімната: {room}
День: {data["stanytsia_day"]}
Час: {data["stanytsia_start_time"]} - {data["stanytsia_end_time"]}
''', reply_markup=create_cancel_button(user_db_obj['user_id'], response['event'].get('id', 'no_code'), 'С'))

        else:
            await message.answer(
                "Сталася помилка при додаванні події.☹️ Спробуйте ще раз або зверніться до офісу Пласту @lvivplastoffice.",
            reply_markup=keyboards.mainkb)
            await state.clear()
