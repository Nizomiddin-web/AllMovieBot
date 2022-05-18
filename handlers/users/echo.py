import os
import re

from keyboards.inline.subcribInline import subsButton
from loader import bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from loader import dp
from utils.db_api.model import get_movie_code_id
from utils.misc import subscription

REGEX = f""


@dp.callback_query_handler(text="check_subs")
async def subscriptions(msg:types.CallbackQuery):
    f = open('data/chanels/chanel.txt', 'r')
    read = f.read()
    f.close()
    read = read.split('\n')
    read.pop()
    arr = []
    for channel in read:
        status = await subscription.check(user_id=msg.from_user.id, channel=channel)
        if not status:
            chanel = await bot.get_chat(channel)
            arr.append(await chanel.export_invite_link())
    if len(arr) < 1:
        await msg.message.delete()
        await msg.message.answer("<b>Botdan to'liq foydalanishingiz mumkin!</b>")
        return
    # subBtn = await subsButton(values=arr)
    await msg.answer(f"❗️ To'liq bajaring ❗️\n\n👉 Sizga kerakli kinoni korish uchun kanalarga obuna bolishingiz "
                     f"kerak.\n\nQuyidagi kanalarga obuna boling👇 \nva tekshirish uchun OBUNA BO'LDIM tugmasini "
                     f"bosing!",show_alert=True)

@dp.message_handler(regexp=re.compile(r"[0-9]"))
async def find_movie(msg: types.Message):
    code_id = msg.text
    if os.stat("data/chanels/chanel.txt").st_size == 0:
        try:
            all = await get_movie_code_id(code_id)
            await msg.answer_video(video=all.id,
                                   caption=f"<b>🔢 Film kodi:</b> #{all.code_id}\n<b>📄 Film Nomi:</b>{all.name}\n\nBy @mybot")
        except:
            await msg.answer(f"⚠️ <b>{code_id}</b> kodi mavjud emas.")
        return
    f = open('data/chanels/chanel.txt', 'r')
    read = f.read()
    f.close()
    read = read.split('\n')
    read.pop()
    arr = []
    for channel in read:
        status = await subscription.check(user_id=msg.from_user.id, channel=channel)
        print(status)
        if not status:
            chanel = await bot.get_chat(channel)
            arr.append(await chanel.export_invite_link())
    if len(arr) < 1:
        try:
            all = await get_movie_code_id(code_id)
            await msg.answer_video(video=all.id,
                                   caption=f"<b>🔢 Film kodi:</b> #{all.code_id}\n<b>📄 Film Nomi:</b>{all.name}\n\nBy @KinoYukladiBot")
        except:
            await msg.answer(f"⚠️ <b>{code_id}</b> kodi mavjud emas.")
        return
    subBtn = await subsButton(values=arr)
    await msg.answer(f"<b>❌ TAYORMASSIZ ❌</b>\n\n👉 Sizga kerakli kinoni korish uchun kanalarga obuna bolishingiz "
                     f"kerak.\n\nQuyidagi kanalarga obuna boling👇 \nva tekshirish uchun <b>OBUNA BO'LDIM</b> tugmasini "
                     f"bosing!", reply_markup=subBtn)



