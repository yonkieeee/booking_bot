from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

return_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Заповнити заново")],
        [KeyboardButton(text="Повернутись до меню")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)