from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_cancel_button(user_id, code_of_booking, domivka):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text='Скасувати бронювання',
                                 callback_data=f'cancel_{code_of_booking}_{user_id}_{domivka}')
        ]],
        one_time_keyboard=True
    )
    return kb


return_kb = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Повернутись до меню")
    ]],
    resize_keyboard=True,
    one_time_keyboard=True
)