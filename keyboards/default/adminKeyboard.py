from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

adminButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Send Users"),
            KeyboardButton(text="Send Groups"),
        ],
        [KeyboardButton(text="Statistic"),
         KeyboardButton(text="🔙exit")
         ]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙ortga")
        ]
    ],
    resize_keyboard=True
)
