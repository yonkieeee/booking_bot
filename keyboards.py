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

approovancebuilder = InlineKeyboardBuilder()
approovancebuilder.add(
    InlineKeyboardButton(text="Так, погоджуюсь", callback_data="approoved"),
    InlineKeyboardButton(text="Ні", callback_data="non_approoved")
)

bookingk = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text="Шептицьких, 16", callback_data="stanytsia")],
        [InlineKeyboardButton(text="Вишкільний цент у Винниках", callback_data="vynnyky")],
        [InlineKeyboardButton(text="Хоткевича, 16А", callback_data="khotkevycha")],
        [InlineKeyboardButton(text="Тютюнників, 25", callback_data="tyutyunnykiv")],
        [InlineKeyboardButton(text="Коциловського, 16", callback_data="kotsylovskogo")],
        [InlineKeyboardButton(text="Котляревського, 17", callback_data="kotlyarevskogo")],
        [InlineKeyboardButton(text="Житомирська, 12", callback_data="zhytomyrska")],
        [InlineKeyboardButton(text="Хочу отримати лист-дозвіл на інше приміщення", callback_data="lysty")]
    ]

)

stanytsiakb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingStanytsia"),
            InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
        ]
    ]
)

vynnykykb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingVynnyky"),
            InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
        ]
    ]
)

khotkevychakb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingKhotkevycha"),
            InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
        ]
    ]
)
tyutyunnykivkb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingTyutyunnykiv"),
            InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
        ]
    ]
)
kotsylovskogokb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingKotsylovskogo"),
            InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
        ]
    ]
)
kotlyarevskogokb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingKotlyarevskogo"),
            InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
        ]
    ]
)

zhytomyrskakb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingStanytsia"),
            InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
        ]
    ]
)
#                       bookingkeyboards                      #
###############################################################
