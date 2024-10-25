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


@router.message(CommandStart() or Command("menu"))
async def start(message: Message, state: FSMContext):
    user_info = db.get_user(message.from_user.id)
    if not db.user_exists(message.from_user.id):
        await message.answer('''СКОБ! Привіт! Давай знайомитись :)
 
🤖 Я чат-бот станиці Львів. Вмію бронювати кімнати, а ще допоможу тобі знайти відповіді на всілякі запитання стосовно наших приміщень 🏠

✅  Аби я міг бронювати кімнати на твоє ім’я спочатку мені необхідно тебе зареєструвати. Для цього дай згоду на обробку персональних даних 👤''',
                             reply_markup=kb.agree_button
                             )
    else:
        await state.clear()
        await message.answer("""Чим я можу допомогти?""", reply_markup=keyboards.mainkb)


@router.message(F.text == 'Погоджуюсь')
async def start_of_reg(message: Message, state: FSMContext):
    await message.answer("Тепер введи своє ім’я та прізвище")
    await state.set_state(registrate_user.user_fullname)


@router.message(F.text == 'Заповнити заново')
async def start_of_reg(message: Message, state: FSMContext):
    reg_info.clear()
    await message.answer("Введи своє ім'я та прізвище")
    await state.set_state(registrate_user.user_fullname)


@router.message(registrate_user.user_fullname)
async def reg_surname(message: Message, state: FSMContext):
    if bools.check_fullname(message.text):
        reg_info.append(message.text)
        await message.answer("Дату народження у форматі ДД.MM.РРРР\n📆 Наприклад: 30.12.2001")
        await state.set_state(registrate_user.user_age)
    else:
        await message.answer("Ти ввів не правильно своє ім'я та прізвище. Спробуй ще раз")


@router.message(registrate_user.user_age)
async def reg_age(message: Message, state: FSMContext):
    if bools.check_age_num(message.text):
        reg_info.append(message.text)
        await message.answer("Поділись своїм номером телефону ☎️",
                             reply_markup=kb.phone_kb)
        await state.set_state(registrate_user.user_phone)
    else:
        await message.answer("Ти ввів не правильно свою дату народження. Спробуй ще раз")


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
    if message.from_user.id == "719886646":
        await message.answer_photo("https://t.me/c/1544453874/41907")
        await message.answer("Здаров чушпан")
        await message.answer_photo("https://t.me/c/1544453874/47740")

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


@router.message(F.text == "Хто розробник цього лайна?")
async def trash(message: Message):
    await message.answer("@naza_rko")


