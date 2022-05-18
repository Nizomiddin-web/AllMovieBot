from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot
from utils.db_api.model import new_user_add


@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.SUPERGROUP))
async def show_channels(message: types.Message):
    try:
        await new_user_add(message.chat.id, 'group', 'true')
    except:
        pass
    text = f"<b><i>Assalomu alaykum, {message.from_user.full_name}\n\nTikTokdan video yuklash uchun 🔗 link yuboring!!!</i></b>"
    await message.answer(text)


@dp.message_handler(CommandStart(), filters.ChatTypeFilter(types.ChatType.GROUP))
async def show_channels(message: types.Message):
    try:
        await new_user_add(message.chat.id, 'group', 'true')
    except:
        pass
    text = f"<b><i>Assalomu alaykum, {message.from_user.full_name}\n\nTikTokdan video yuklash uchun 🔗 link yuboring!!!</i></b>"
    await message.answer(text)
