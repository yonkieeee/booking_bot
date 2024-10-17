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
            KeyboardButton(text="🔐Забронюй кімнату"),
            KeyboardButton(text="Мої бронювання✍🏻")
        ],
        [
            KeyboardButton(text='Переглянути профіль')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Чим я можу допомогти?",
    selective=True
)

##############################################################
#                       bokingkeyboards                      #

approovancebuilder = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Погоджуюсь із правилами", callback_data="approoved"),
            InlineKeyboardButton(text="Не погоджуюсь", callback_data="non_approoved")
        ]
    ]
)

approovancebuilder_v = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Погоджуюсь із правилами", callback_data="approoved_v"),
            InlineKeyboardButton(text="Не погоджуюсь", callback_data="non_approoved")
        ]
    ]
)

bookingk = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text="Шептицьких, 16", callback_data="stanytsia")],
        [InlineKeyboardButton(text="Вишкільний центр у Винниках", callback_data="vynnyky")]
    ]

)

stanytsiakb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingStanytsia"),
            InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/ksvs3bv65cgver4o6q")
        ]
    ]
)

room_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="201", callback_data="201"),
            InlineKeyboardButton(text="206", callback_data="206"),
        ],
        [
            InlineKeyboardButton(text="208", callback_data="208"),
            InlineKeyboardButton(text="303", callback_data="303"),
        ],
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
vynnyky_room_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
           InlineKeyboardButton(text="Кухня", callback_data="Кухня"),
        ],
        [
            
            InlineKeyboardButton(text="Поверх 1", callback_data="Поверх 1"),
        ],
        [
            InlineKeyboardButton(text="Поверх 2, кімната 1", callback_data="Поверх 2, кімната 1"),
        ],
        [
            InlineKeyboardButton(text="Поверх 2, кімната 2", callback_data="Поверх 2, кімната 2"),
        ],
        [
            InlineKeyboardButton(text="Поверх 2, кімната 3", callback_data="Поверх 2, кімната 3"),
        ],
        [
            InlineKeyboardButton(text="Поверх 2, кімната 4", callback_data="Поверх 2, кімната 4"),
        ],
        
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
