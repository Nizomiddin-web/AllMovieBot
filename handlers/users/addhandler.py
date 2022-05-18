import os
import re
from time import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.default.adminKeyboard import adminButton, back
from keyboards.inline.addInline import addButtonsInline, bekorqilish, addLimitButtonsInline
from loader import dp
from states.adminState import AdminState, AddState
from utils.db_api.model import getUserList, getUsersCount, getGroupList, getGroupsCount, new_movie_add
from aiogram.types import ReplyKeyboardRemove

"""Yangi Qo'shish bo'limi"""


@dp.message_handler(commands='add')
async def add_command(msg: types.Message):
    user_id = msg.from_user.id
    if str(user_id) in ADMINS:
        await msg.reply("Salom Xurmatli admin siz quyidagilardan birini tanlashingiz mumkin!",
                        reply_markup=addButtonsInline)
        return
    if os.stat("data/admin/admin.txt").st_size == 0:
        await msg.reply("<b>Siz noto'g'ri buyruq kiritdingiz!</b>")
        return
    f = open('data/admin/admin.txt', 'r')
    read = f.read()
    read = read.split('\n')
    f.close()
    if str(user_id) in read:
        await msg.reply("Salom Xurmatli admin siz siz quyidagilardan birini tanlashingiz mumkin!",
                        reply_markup=addLimitButtonsInline)
    else:
        await msg.reply("<b>Siz noto'g'ri buyruq kiritdingiz!</b>")


@dp.callback_query_handler(text="addChanel")
async def add_channel(msg: types.CallbackQuery):
    await msg.bot.edit_message_text(
        "Ulamoqchi bo'lgan <i>Kanal</i> <b>Username</b> yoki <b> IDsi</b>ni yuboring!", msg.from_user.id,
        msg.message.message_id)
    await msg.bot.edit_message_reply_markup(msg.from_user.id, msg.message.message_id, reply_markup=bekorqilish)
    await AddState.addChanelState.set()


@dp.callback_query_handler(text="addMovie")
async def add_Movie(msg: types.CallbackQuery):
    await msg.message.delete()
    # await msg.bot.send_photo(msg.from_user.id, "AgACAgIAAxkBAAEP1VFihA-kgdED-pg_2CxGViWHLb2CtwACSb8xG"
    #                                            "-N0IEhdM8_sTwcqzgEAAwIAA20AAyQE",
    #                          caption="<b>Videoni ID va Nomi yozilish "
    #                                  "tartibi!</b>")
    await msg.message.answer(
        "<b>Qo'shmoqchi bo'lgan Videongizni yuboring!\n\nVideo ID si va Nomi bo'lishi Shart!</b>",
        reply_markup=bekorqilish)
    await AddState.addMovieState.set()


@dp.callback_query_handler(text="addAdmin")
async def add_channel(msg: types.CallbackQuery):
    await msg.bot.edit_message_text(
        "Qo'shmoqchi bo'lgan <b>Admin ID</b>sini yuboring!", msg.from_user.id,
        msg.message.message_id)
    await msg.bot.edit_message_reply_markup(msg.from_user.id, msg.message.message_id, reply_markup=bekorqilish)
    await AddState.addAdminState.set()


@dp.callback_query_handler(state=AddState.addMovieState, text="cancel")
@dp.callback_query_handler(state=AddState.addAdminState, text="cancel")
@dp.callback_query_handler(state=AddState.addChanelState, text="cancel")
@dp.callback_query_handler(state=AddState.delChanel, text="cancel")
async def cancel(msg: types.CallbackQuery, state: FSMContext):
    user_id = msg.from_user.id
    if str(user_id) in ADMINS:
        await msg.bot.edit_message_text(
            "<b>❌ Bekor qilindi!</b>", msg.from_user.id,
            msg.message.message_id)
        await msg.bot.edit_message_reply_markup(msg.from_user.id, msg.message.message_id, reply_markup=addButtonsInline)
        await state.finish()
        return
    if os.stat("data/admin/admin.txt").st_size == 0:
        await msg.message.delete()
        await msg.bot.send_message(msg.from_user.id, "<b>Siz noto'g'ri buyruq kiritdingiz!</b>")
        await state.finish()
        return
    f = open('data/admin/admin.txt', 'r')
    read = f.read()
    read = read.split('\n')
    f.close()
    if str(user_id) in read:
        await msg.bot.edit_message_text(
            "<b>❌ Bekor qilindi!</b>", msg.from_user.id,
            msg.message.message_id)
        await msg.bot.edit_message_reply_markup(msg.from_user.id, msg.message.message_id,
                                                reply_markup=addLimitButtonsInline)
        await state.finish()
    else:
        await msg.message.delete()
        await msg.bot.send_message(msg.from_user.id, "<b>Siz noto'g'ri buyruq kiritdingiz!</b>")
        await state.finish()


"""Movie qo'shish qatori"""


@dp.message_handler(state=AddState.addMovieState, content_types=types.ContentTypes.VIDEO)
async def add_movie(msg: types.Message, state: FSMContext):
    try:
        result = msg.caption.split(f"\n")
        id = result[0]
        name = result[1]
        file_id = msg.video.file_id
    except:
        await msg.answer("Kinoning id yoki nomi berilmagan!\n Iltimos qayta harakat qiling!")
        return
    try:
        await new_movie_add(id=file_id, code_id=id, name=name)
        await msg.answer(f"<b>✅ Kino bazaga saqlandi!</b>\n\n {id} kodi orqali topishingiz mumkin!")
        await state.finish()
    except:
        await msg.answer("<b>Bazaga saqlanmadi! \nQaytadan urinib ko'ring!\n\nEslatma code bir xil bo'lgan kinolar "
                         "bazaga saqlanmaydi! </b>")


"""Admin qo'shish qatori"""


@dp.message_handler(state=AddState.addAdminState, regexp=re.compile(r'[0-9]'))
async def add_admin(msg: types.Message, state: FSMContext):
    admin = msg.text
    f = open('data/admin/admin.txt', 'a')
    f.write(f"{admin}\n")
    f.close()
    await msg.answer("<b>Yangi Admin muvafaqiyatli qo'shildi✅</b>")
    try:
        await msg.bot.send_message(admin, "Siz <b>SuperAdmin</b> tomonidan  <b>Admin</b> etib tayinlandingiz "
                                          "🥳\n\n<b>Buyruqlar:</b>\n/add- <b>Kanal</b> yoki <b>Kino</b> qo'shish\n\n/del- <b>Kanal</b> "
                                          "ni o'chirish")
    except:
        pass
    await state.finish()


"""Kanal qo'shish qatori"""


@dp.message_handler(state=AddState.addChanelState, regexp=re.compile(r'[0-9]'))
async def add_admin(msg: types.Message, state: FSMContext):
    chat_id = f"-100{msg.text}"
    try:
        id= await msg.bot.get_chat_member(chat_id=chat_id, user_id=msg.from_user.id)
        chanel = await msg.bot.get_chat(chat_id=chat_id)
        f = open("data/chanels/chanel.txt", "a")
        f.write(f"{chanel.id}\n")
        f.close()
        await msg.answer("<b>Kanal qo'shildi✅</b>")
        await state.finish()
    except:
        await msg.reply("Bot bu <b>Kanalda</b> admin qilinmagan!\n\nQayta <b>Kanal ID</b> jo'nating!",
                        reply_markup=bekorqilish)


@dp.message_handler(state=AddState.addChanelState, content_types=types.ContentTypes.TEXT)
async def add_admin(msg: types.Message, state: FSMContext):
    if msg.text.startswith("t.me/"):
        channelUser = msg.text.split("/")
        channelUser = channelUser[1]
    elif msg.text.startswith("https://t.me/"):
        channelUser = msg.text.split("/")
        channelUser = channelUser[3]
    elif msg.text.startswith("@"):
        channelUser = msg.text.split("@")
        channelUser = channelUser[1]
    else:
        channelUser = msg.text
    channelUser = f"@{channelUser}"
    try:
        id = await msg.bot.get_chat_member(chat_id=channelUser, user_id=msg.from_user.id)
        print(id)
        chanel = await msg.bot.get_chat(chat_id=channelUser)
        f = open("data/chanels/chanel.txt", "a")
        f.write(f"{chanel.id}\n")
        f.close()
        await msg.answer("Chanel qo'shildi")
        await state.finish()
    except:
        await msg.reply("Bot bu Kanalda Admin emas!\n\nQayta Kanal jo'nating!", reply_markup=bekorqilish)


"""Admin Commandalar qatori"""
