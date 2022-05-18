from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot

submitInline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Kanalga joylash✅", callback_data="send"),
            InlineKeyboardButton(text="Cansel❌", callback_data="cansel")
        ]
    ]
)

delButtonsInline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Delete Chanel ❌", callback_data="delChanel"),
        ],
        [
            InlineKeyboardButton(text="❌ Delete Admin ❌", callback_data="delAdmin"),
        ]
    ]
)

delLimitButton = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Delete Chanel ❌", callback_data="delChanel"),
        ]
    ]
)


async def delAdminsButton(values):
    btnInl = InlineKeyboardMarkup(row_width=1)
    i = 0
    for val in values:
        btnKeyboard = InlineKeyboardButton(text=val, callback_data=val)
        btnInl.insert(btnKeyboard)
        i += 1
    bekor = InlineKeyboardButton("Bekor qilish", callback_data="cancel")
    btnInl.insert(bekor)
    return btnInl


async def delChanelsButton(values):
    btnInl = InlineKeyboardMarkup(row_width=1)
    i = 0
    for val in values[0:len(values) - 1]:
        chanel = await bot.get_chat(chat_id=val)
        btnKeyboard = InlineKeyboardButton(text=chanel.title, callback_data=val)
        btnInl.insert(btnKeyboard)
        i += 1
    bekor = InlineKeyboardButton("Bekor qilish", callback_data="cancel")
    btnInl.insert(bekor)
    return btnInl
