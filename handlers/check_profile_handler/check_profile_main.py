from aiogram import Router, F, Bot
from aiogram import types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from handlers.start_menu.user_db import DataBase
from handlers.start_menu.start import registrate_user
from handlers.check_profile_handler.check_kb import return_kb
import bots

router = Router()
db = DataBase('db_plast.db')
bot = Bot(bots.main_bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

reg_user = registrate_user()


@router.message(F.text.lower() == 'переглянути профіль')
async def check_profile(message: types.Message):
    info = db.get_user(str(message.from_user.id))

    if info['user_nickname'] is None:
        nickname_text = ''
    else:
        nickname_text = f'\nНікнейм: {info["user_nickname"]}'

    await message.answer(f'''ID: {message.from_user.id}{nickname_text}

Ім'я: {info['user_name']}
Прізвище: {info['user_surname']}
Рік народження: {info['user_age']}
Номер телефону: {info['user_phone']}''', reply_markup=return_kb)

