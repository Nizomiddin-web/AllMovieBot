from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def subsButton(values):
    btnInl = InlineKeyboardMarkup(row_width=1)
    i = 0
    for channel in values:
        btnKeyboard = InlineKeyboardButton(text=f"{i+1}-Kanal", url=channel)
        btnInl.insert(btnKeyboard)
        i += 1
    azoCheck = InlineKeyboardButton("Obuna bo'ldim✅", callback_data="check_subs")
    btnInl.insert(azoCheck)
    return btnInl
