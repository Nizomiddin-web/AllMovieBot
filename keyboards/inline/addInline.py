from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, inline_keyboard

addButtonsInline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="addChanel"),
            InlineKeyboardButton(text=" Film qo'shish 🎥", callback_data="addMovie"),
        ],
        [
            InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="addAdmin"),
        ]
    ]
)

addLimitButtonsInline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="addChanel"),
            InlineKeyboardButton(text=" Film qo'shish 🎥", callback_data="addMovie"),
        ]
    ]
)


bekorqilish = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Bekor qilish", callback_data="cancel")]
    ]
)
