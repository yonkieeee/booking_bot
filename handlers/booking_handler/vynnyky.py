
import asyncio
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
from . import booking_menu
from .booking_menu import Bookingreg

router = Router()

bot = Bot(bots.main_bot, default=DefaultBotProperties(parse_mode="HTML"))


class Vynnyky_Bookingreg(Bookingreg):
    pass

@router.callback_query(F.data == "vynnyky")
async def bookstanytsia(callback: types.CallbackQuery):
    await callback.message.answer("Перед натисканням на кнопку 'Реєстрація бронювання' переглянь графік", reply_markup=keyboards.vynnykykb)
    

@router.callback_query(F.data == "RegistrateBookingVynnyky")
async def reg_vynnyky_one(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Vynnyky_Bookingreg.booking_name)
    await bot.send_message(chat_id=callback.from_user.id, text="Введіть назву події")
    print("Поточний стан:", Vynnyky_Bookingreg.booking_name)

@router.message(Vynnyky_Bookingreg.booking_name)
async def reg_vynnyky_two(message: Message, state: FSMContext):
    # Зберігаємо дані в стан
    await state.update_data(booking_name=message.text)

    # Друкуємо значення, яке ввів користувач
    print("Назва події:", message.text)
    
    await state.set_state(Vynnyky_Bookingreg.number_of_room)
    await message.answer("Обери номер кімнати", reply_markup=keyboards.vynnyky_rooms)

@router.message(Vynnyky_Bookingreg.number_of_room)
async def reg_vynnyky_three(message: Message, state: FSMContext):
    await state.update_data(number_of_room=message.text)
    await state.set_state(Vynnyky_Bookingreg.day)
    await message.answer("Введіть день у форматі РРРР-ММ-ДД. Наприклад: 2024-05-20")

@router.message(Vynnyky_Bookingreg.day)
async def reg_vynnyky_four(message: Message, state: FSMContext):
    await state.update_data(day=message.text)
    await state.set_state(Vynnyky_Bookingreg.start_time)
    await message.answer("Введіть час початку у форматі ГГ:ХХ. Наприклад 15:00")

@router.message(Vynnyky_Bookingreg.start_time)
async def reg_vynnyky_five(message: Message, state: FSMContext):
    await state.update_data(start_time=message.text)
    await state.set_state(Vynnyky_Bookingreg.end_time)
    await message.answer("Введіть час закінчення у форматі ГГ:ХХ. Наприклад 16:00")

@router.message(Vynnyky_Bookingreg.end_time)
async def reg_vynnyky_six(message: Message, state: FSMContext):
    await state.update_data(end_time=message.text)
    data = await state.get_data()
    if data["number_of_room"] == "кімната 1":
        vynnyky_subid = 13281316
    elif data["number_of_room"] == "кімната 2":
        vynnyky_subid = 13281315
    else:
        await message.answer("Ви ввели неправильний номер кімнати. Зареєструйте бронювання ще раз.")
        await state.set_state(Vynnyky_Bookingreg.booking_name)
        await bot.send_message(chat_id=message.from_user.id, text="Введіть назву події")
        return

    start_datetime = f'{data["day"]}T{data["start_time"]}:00Z'
    end_datetime = f'{data["day"]}T{data["end_time"]}:00Z'

    if await booking_menu.check_event_conflicts(start_datetime, end_datetime, calendars.VYNNYKY_TEAMUP_API_KEY):
        await message.answer("Це приміщення зайняте в цей час. Оберіть інший час.")
        await state.clear()
    else:
        response = await booking_menu.add_calendar_event(data, calendars.VYNNYKY_TEAMUP_API_KEY, calendars.VYNNYKY_TEAMUP_CALENDAR_ID, vynnyky_subid)
        if 'event' in response:
            db = db_booking.Booking_DataBase("db_plast.db")
            db.add_book_reg(
                user_id=message.from_user.id,
                user_name=message.from_user.first_name, 
                user_surname=message.from_user.last_name,  
                user_domivka="vynnyky",
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



