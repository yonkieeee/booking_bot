
from aiogram.types import (
ReplyKeyboardMarkup,
KeyboardButton,
InlineKeyboardMarkup,
InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

phone_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поділитись контактом", request_contact=True)]
])
