from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

start_reg = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Зареєструватись",
                   )]
],
    resize_keyboard=True,
    one_time_keyboard=True
)

phone_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поділитись контактом", request_contact=True)]
],
    resize_keyboard=True,
    one_time_keyboard=True
)

agree_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Погоджуюсь')]
],
    resize_keyboard=True,
    one_time_keyboard=True
)