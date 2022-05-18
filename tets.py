import os
import re
from time import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.inline.addInline import bekorqilish
from keyboards.inline.delInline import delButtonsInline, delAdminsButton, delLimitButton
from loader import dp
from states.adminState import AdminState, AddState
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(commands='del')
async def add_command(msg: types.Message):
    user_id = msg.from_user.id
    if str(user_id) in ADMINS:
        await msg.reply("Salom Xurmatli admin siz siz quyidagilardan birini tanlashingiz mumkin!",
                        reply_markup=delButtonsInline)
    if os.stat("data/admin/admin.txt").st_size == 0:
        await msg.reply("<b>Siz noto'g'ri buyruq kiritdingiz!</b>")
        return
    f = open('data/admin/admin.txt', 'r')
    read = f.read()
    read = read.split('\n')
    f.close()
    if str(user_id) in read:
        await msg.reply("Salom Xurmatli admin siz siz quyidagilardan birini tanlashingiz mumkin!",
                        reply_markup=delLimitButton)
        return
    await msg.reply("<b>Siz noto'g'ri buyruq kiritdingiz!</b>")


@dp.callback_query_handler(text="delChanel")
async def del_channel(msg: types.Message):
    pass


@dp.callback_query_handler(text="delMovie")
async def del_Movie(msg: types.CallbackQuery):
    await msg.bot.edit_message_text(
        "<b>Qo'shmoqchi bo'lgan Videongizni yuboring!\n\nVideo ID si va Nomi bo'lishi Shart!</b>", msg.from_user.id,
        msg.message.message_id)
    await msg.bot.edit_message_reply_markup(msg.from_user.id, msg.message.message_id, reply_markup=bekorqilish)
    await AddState.addMovieState.set()


"""Admin O'chirish qatori"""


@dp.callback_query_handler(text="delAdmin")
async def add_channel(msg: types.CallbackQuery):
    if os.stat("data/admin/admin.txt").st_size == 0:
        await msg.bot.edit_message_text("Sizda adminlar mavjud emas!", msg.from_user.id,
                                        msg.message.message_id)
        return
    await msg.bot.edit_message_text(
        "O'chirilishi kerak bo'lgan <b>Admin ID</b>sini Ustiga Bosing!", msg.from_user.id,
        msg.message.message_id)
    f = open('data/admin/admin.txt', 'r')
    read = f.read()
    read = read.split('\n')
    f.close()
    print(read)
    adminBtn = await delAdminsButton(read)
    await msg.bot.edit_message_reply_markup(msg.from_user.id, msg.message.message_id, reply_markup=adminBtn)
    await AddState.addAdminState.set()


@dp.callback_query_handler(state=AddState.addAdminState, regexp=re.compile(r'[0-9]'))
async def add_admin(msg: types.CallbackQuery, state: FSMContext):
    admin = msg.data
    f = open('data/admin/admin.txt', 'r')
    read = f.read()
    f.close()
    read = read.split('\n')
    read.pop()
    if admin in read:
        read.remove(admin)
        print(read)
        f = open('data/admin/admin.txt', 'w')
        text = str()
        for i in read:
            text+=f"{i}\n"
        f.write(f"{text}")
        f.close()
        await msg.answer("<b>Admin Olib tashlandi!</b>")
        await state.finish()
    else:
        await msg.answer("Siz mavjud bo'lmagan <b>ID</b> kiritdingiz!\nMavjud ID ni yuboring!")