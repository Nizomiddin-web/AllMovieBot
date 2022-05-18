from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

postLangKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🇺🇿O'zbek tilida"),
            KeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿Ingliz tilida")
        ],
        [
            KeyboardButton("🇷🇺Rus tilida")
        ]
    ],
    resize_keyboard=True
)
