from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.filters import Command, CommandStart, or_f
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from calendars import get_subcalendars
from calendars import STANYTSIA_TEAMUP_API_KEY, STANYTSIA_TEAMUP_CALENDAR_ID, VYNNYKY_TEAMUP_API_KEY, VYNNYKY_TEAMUP_CALENDAR_ID

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
            InlineKeyboardButton(text="Зареєструвати бронювання", callback_data="RegistrateBookingStanytsia"),
            InlineKeyboardButton(text="Календар бронювань", url="https://teamup.com/ksvs3bv65cgver4o6q")
        ]
    ]
)

book_again = InlineKeyboardMarkup(
    inline_keyboard=[
        [
        InlineKeyboardButton(text="Спробувати ще раз", callback_data="RegistrateBookingStanytsia")
        ]
    ]
)
stanytsia_rooms_builder = InlineKeyboardBuilder()
rooms=get_subcalendars(STANYTSIA_TEAMUP_CALENDAR_ID, STANYTSIA_TEAMUP_API_KEY)
for key in rooms:
    stanytsia_rooms_builder.button(text=key,callback_data=key)
stanytsia_rooms_builder.adjust(2)


vynnykykb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Зареєструвати бронювання", callback_data="RegistrateBookingVynnyky"),
            InlineKeyboardButton(text="ГКалендар бронювань", url="https://teamup.com/ksnkruqk4d9xezc8r7")
        ]
    ]
)

vynnykybooking_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Написати на офіс", url="https://t.me/lvivplastoffice")
           
            
        ]
    ]
)


# vynnyky_rooms_builder = InlineKeyboardBuilder()
# rooms=get_subcalendars(VYNNYKY_TEAMUP_CALENDAR_ID, VYNNYKY_TEAMUP_API_KEY)
# for key in rooms:
#     vynnyky_rooms_builder.button(text=key,callback_data=key)
# vynnyky_rooms_builder.adjust(2)

# khotkevychakb = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingKhotkevycha"),
#             InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
#         ]
#     ]
# )
# tyutyunnykivkb = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingTyutyunnykiv"),
#             InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
#         ]
#     ]
# )
# kotsylovskogokb = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingKotsylovskogo"),
#             InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
#         ]
#     ]
# )
# kotlyarevskogokb = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingKotlyarevskogo"),
#             InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
#         ]
#     ]
# )

# zhytomyrskakb = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Реєстрація бронювання", callback_data="RegistrateBookingStanytsia"),
#             InlineKeyboardButton(text="Графік Бронювання", url="https://teamup.com/kstbv5srw3gter52zv")
#         ]
#     ]
# )
#                       bookingkeyboards                      #
###############################################################
