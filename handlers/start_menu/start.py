from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from handlers.start_menu.user_db import DataBase
from handlers.start_menu import bools
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from handlers.start_menu import start_keyboard as kb
import keyboards

router = Router()
db = DataBase("db_plast.db")
reg_info = []


class registrate_user(StatesGroup):
    user_name = State()
    user_surname = State()
    user_age = State()
    user_phone = State()
    user_email = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if not db.user_exists(message.from_user.id):
        await message.answer('''Привіт 👋, я бот для бронювань приміщень Пласту у Львові!" 
З моєю допомогою ти зможеш: 
    📍 Забронювати приміщення в пластовій домівці 
    📍 Воно одразу з'явиться в календарі бронювання 
    📍 Тобі не потрібно чекати на відповідь адміна 
    📍 Зможеш обрати зручний час та зробити бронювання самостійно  
    📍Є можливість перегляду активних бронювань та скасувати їх за потреби 
Якщо ти хочеш скористатись ботом, тобі необхідно зареєструватись. Так нам буде простіше співпрацювати далі🤝''',
                             reply_markup=kb.start_reg
                             )

    else:
        await message.answer("Обери секцію", reply_markup=keyboards.mainkb)


@router.message(F.text == 'Зареєструватись')
async def start_of_reg(message: Message, state: FSMContext):
    await message.answer("Введи своє ім'я")
    await state.set_state(registrate_user.user_name)


@router.message(F.text == 'Заповнити заново')
async def start_of_reg(message: Message, state: FSMContext):
    db.user_delete(message.from_user.id)
    await message.answer("Введи своє ім'я")
    await state.set_state(registrate_user.user_name)


@router.message(registrate_user.user_name)
async def reg_name(message: Message, state: FSMContext):
    if not bools.find_symbol(message.text):
        reg_info.append(message.text)
        await message.answer("Введи своє прізвище")
        await state.set_state(registrate_user.user_surname)
    else:
        await message.answer("fef")


@router.message(registrate_user.user_surname)
async def reg_surname(message: Message, state: FSMContext):
    if not bools.find_symbol(message.text):
        reg_info.append(message.text)
        await message.answer("Введи свою дату народження(DD.MM.YYYY)")
        await state.set_state(registrate_user.user_age)
    else:
        await message.answer("fef")


@router.message(registrate_user.user_age)
async def reg_age(message: Message, state: FSMContext):
    if bools.check_age_num(message.text):
        reg_info.append(message.text)
        await message.answer("Поділись своїм номером телефону ☎️",
                             reply_markup=kb.phone_kb)
        await state.set_state(registrate_user.user_phone)
    else:
        await message.answer("fef")


@router.message(registrate_user.user_phone)
async def reg_phone(message: Message, state: FSMContext):
    reg_info.append(message.contact.phone_number)
    await message.answer("Введи свою електронну адресу 📧",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(registrate_user.user_email)


@router.message(registrate_user.user_email)
async def reg_email(message: Message, state: FSMContext):
    email_domain = ['@gmail.com', '@ukr.net', '@icloud.com', '@outlook.com']
    if any(domain in message.text for domain in email_domain):
        reg_info.append(message.text)

        name, surname, age, phone, email = reg_info

        db.add_user(user_id=message.from_user.id,
                    user_nickname=message.from_user.username,
                    user_name=name,
                    user_surname=surname,
                    user_age=age,
                    user_phone=phone,
                    user_email=email)

        reg_info.clear()

        await message.answer("Реєстрація завершена✔️", reply_markup=keyboards.mainkb)
        await state.clear()
    else:
        await message.answer("Помилка. Введи існуючу пошту")


# @router.message()
# async def trash(message: Message):
#     await message.answer("Не розумію тебе")


@router.message(Command("menu"))
async def start(message: Message):
    await message.answer("Обери секцію", reply_markup=keyboards.mainkb)
