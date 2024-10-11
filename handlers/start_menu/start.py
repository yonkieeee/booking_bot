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
    user_fullname = State()
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
        await message.answer("""Чим я можу допомогти?

🔐 Забронюй кімнату / Покажи календар бронювань 📆""", reply_markup=keyboards.mainkb)


@router.message(F.text == 'Зареєструватись')
async def start_of_reg(message: Message, state: FSMContext):
    await message.answer("Перед початком реєстрації мені потрібна твоя згода про обробку персональних данних",
                         reply_markup=kb.agree_button)


@router.message(F.text == 'Погоджуюсь')
async def start_of_reg(message: Message, state: FSMContext):
    await message.answer("Введи своє ім'я та прізвище")
    await state.set_state(registrate_user.user_fullname)


@router.message(F.text == 'Заповнити заново')
async def start_of_reg(message: Message, state: FSMContext):
    #db.user_delete(message.from_user.id)
    reg_info.clear()
    await message.answer("Введи своє ім'я та прізвище")
    await state.set_state(registrate_user.user_fullname)


@router.message(registrate_user.user_fullname)
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

    fullname, age, phone = reg_info
    name, surname = str(fullname).split()

    print(reg_info)
    if db.user_exists(message.from_user.id):
        db.user_delete(message.from_user.id)

        db.add_user(user_id=message.from_user.id,
                    user_nickname=message.from_user.username,
                    user_name=name,
                    user_surname=surname,
                    user_age=age,
                    user_phone=phone)
    else:
        db.add_user(user_id=message.from_user.id,
                    user_nickname=message.from_user.username,
                    user_name=name,
                    user_surname=surname,
                    user_age=age,
                    user_phone=phone)
    reg_info.clear()

    await message.answer("Реєстрація завершена✔️", reply_markup=keyboards.mainkb)
    await state.clear()
    await state.set_state(registrate_user.user_email)


'''@router.message(registrate_user.user_email)
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
        await message.answer("Помилка. Введи існуючу пошту")'''


# @router.message()
# async def trash(message: Message):
#     await message.answer("Не розумію тебе")


@router.message(Command("menu"))
async def start(message: Message):
    await message.answer("Чим я можу допомогти?", reply_markup=keyboards.mainkb)
