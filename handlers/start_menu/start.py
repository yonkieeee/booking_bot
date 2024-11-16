from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart, or_f
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


@router.message(or_f(CommandStart(), Command("menu")))
async def start(message: Message, state: FSMContext):
    if not db.user_exists(str(message.from_user.id)):
        await message.answer('''Привіт! Давай знайомитись :)

👤 Аби я міг бронювати кімнати на твоє ім’я спочатку мені необхідно тебе зареєструвати

❗️Зверни увагу, що бронювати кімнати можуть лише повнолітні пластуни

✅ Перш ніж розпочати реєстрацію, дай згоду на обробку персональних даних''',
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
    elif str(message.text).split()[0] > 50 or str(message.text).split()[1] > 50:
        await message.answer("Введено забагато символів. Спробуй ще раз")
    else:
        await message.answer("Введено не правильно ім'я або прізвище. Спробуй ще раз")


@router.message(registrate_user.user_age)
async def reg_age(message: Message, state: FSMContext):
    if bools.check_age_num(message.text):
        reg_info.append(message.text)
        await message.answer("Поділись своїм номером телефону(Кнопка нижче) ☎️",
                             reply_markup=kb.phone_kb)
        await state.set_state(registrate_user.user_phone)
    else:
        await message.answer("Ти ввів не правильно свою дату народження. Спробуй ще раз")


@router.message(registrate_user.user_phone)
async def reg_phone(message: Message, state: FSMContext):
    if message.contact.phone_number:
        reg_info.append(message.contact.phone_number)

        fullname, age, phone = reg_info
        name, surname = str(fullname).split()

        print(reg_info)
        if db.user_exists(str(message.from_user.id)):
            db.user_delete(str(message.from_user.id))

            db.add_user(user_id=str(message.from_user.id),
                        user_nickname=message.from_user.username,
                        user_name=name,
                        user_surname=surname,
                        user_age=age,
                        user_phone=phone)
        else:
            db.add_user(user_id=str(message.from_user.id),
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
    else:
        await message.answer("Помилка реєстрації номера. Натисни ще раз кнопку", reply_markup=kb.phone_kb)




@router.message(F.text == "Хто  керівник цього лайна ?")
async def trash(message: Message):
    await message.answer("@naza_rko")



@router.message(F.text == "Курва мач я пердоля")
async def trash(message: Message):
    await message.answer("Бобр курва, яке бидле")


@router.message(F.text == "СКОБ")
async def skob(message: Message):
    await message.answer("Сильно. Красно. Обережно. Бистро.")

@router.message(F.text == "SKOB")
async def skob(message: Message):
    await message.answer("You think I don`t know english?\nStrong. Beautiful. Carefully. Fast\nSBCF")

@router.message(F.text == "Зачитай реп ")
async def mc_petya(message: Message):
    await message.answer("<a href='https://youtube.com/shorts/egLK3Y7L4XM?feature=share'>Реп</a>"
                         ,parse_mode=ParseMode.HTML,
                         disable_web_page_preview=True)



