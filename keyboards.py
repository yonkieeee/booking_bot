from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

mainkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Бронювання"),
            KeyboardButton(text="Глянути всі бронювання")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Обери розділ",
    selective=True
)

##############################################################
#                       bokingkeyboards                      #
bookingk = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text="Шептицьких, 16", callback_data="stanytsia")],
        [InlineKeyboardButton(text="Вишкільний цент у Винниках", callback_data="vynnyky")],
        [InlineKeyboardButton(text="Хоткевича, 16А", callback_data="khotkevycha")],
        [InlineKeyboardButton(text="Тютюнників, 25", callback_data="tyutyunnykiv")],
        [InlineKeyboardButton(text="Коциловського, 16", callback_data="kosylovskogo")],
        [InlineKeyboardButton(text="Котляревського, 17", callback_data="kotlyarevskogo")],
        [InlineKeyboardButton(text="Житомирська, 12", callback_data="zhytomyrska")],
        [InlineKeyboardButton(text="Хочу отримати лист-дозвіл на інше приміщення", callback_data="lysty")]
    ]

)

approovancebuilder = InlineKeyboardBuilder()
approovancebuilder.add(
    InlineKeyboardButton(text="Так, погоджуюсь", callback_data="approoved"),
    InlineKeyboardButton(text="Ні", callback_data="non_approoved")
)

stanytsiakb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookinStanytsia"),
            InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
        ]
    ]
)

#                       bookingkeyboards                      #
###############################################################
