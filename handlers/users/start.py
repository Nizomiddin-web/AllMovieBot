from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import CHANNELS
from keyboards.inline.subcribInline import subsButton
from loader import dp, bot
from utils.db_api.model import new_user_add

@dp.message_handler(commands=["used"])
async def used(message: types.Message):
    text = f"<b><i>🔗 Yuklab olish uchun YouTubedagi videoning havolasini botga yuboring.</i>\n\n📋 Qo'llanma:</b>\n1. YouTube " \
           f"ilovasiga kiring.\n2. Videoni tanlang.\n3. «Ulashish» ni bosing va ochilgan bo'limdan Telegram ilovasini " \
           f"tanlang.\n4. Telegramga kirganingizdan so'ng qidiruv tugmasini bosib, «YouTubeSavedBot» deb yozing. " \
           f"Birinchi natijani \ntanlang. Tayyor ✅ "
    await message.answer(text)


@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.PRIVATE))
async def show_channels(message: types.Message):
    try:
        await new_user_add(message.from_user.id, 'user', 'true')
    except:
        pass
    # ok = await subsButton(channels=CHANNELS,values=CHANNELS)

    text = f"<b><i>Assalomu alaykum, {message.from_user.full_name}\n\nEng sara kinolarni bu yerdan toping!\nBoshlash " \
           f"uchun kino kodini yuboring!</i></b> "
    await message.answer(text)


