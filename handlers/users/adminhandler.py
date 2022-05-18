import os
import re
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.default.adminKeyboard import adminButton, back
from keyboards.inline.addInline import addButtonsInline, bekorqilish, addLimitButtonsInline
from loader import dp
from states.adminState import AdminState, AddState
from utils.db_api.model import getUserList, getUsersCount, getGroupList, getGroupsCount, new_movie_add
from aiogram.types import ReplyKeyboardRemove


"""Admin Commandalar qatori"""


@dp.message_handler(commands='admin')
async def admin_panel(msg: types.Message):
    user_id = msg.from_user.id
    if str(user_id) in ADMINS:
        await msg.reply(f"{msg.from_user.full_name} Admin panelga hush kelibsiz!", reply_markup=adminButton)
        await AdminState.adminState.set()
    else:
        await msg.reply("Siz noto'g'ri buyruq kiritdingiz!")


@dp.message_handler(text="Send Users", state=AdminState.adminState)
async def send_users(msg: types.Message):
    await AdminState.next()
    await msg.reply("Userlarga yuboriladigan habarni kiriting!", reply_markup=back)


@dp.message_handler(text="Send Groups", state=AdminState.adminState)
async def send_users(msg: types.Message):
    await AdminState.SendGroup.set()
    await msg.reply("Userlarga yuboriladigan habarni kiriting!", reply_markup=back)


@dp.message_handler(text="Statistic", state=AdminState.SendUsers)
@dp.message_handler(text="Statistic", state=AdminState.SendGroup)
@dp.message_handler(text="Statistic", state=AdminState.adminState)
async def user_statistic(msg: types.Message):
    rowsUser = await getUsersCount()
    rowsGroup = await getGroupsCount()
    await msg.answer(f"<b>📊 Bot Statistikasi \n\n 👤 Members: {rowsUser}\n👥 Groups: {rowsGroup}</b>")


@dp.message_handler(state=AdminState.adminState, text="🔙exit")
@dp.message_handler(state=AdminState.SendUsers, text="🔙exit")
@dp.message_handler(state=AdminState.SendGroup, text="🔙exit")
async def exit_admin(msg: types.Message, state: FSMContext):
    await msg.answer("Exit", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(state=AdminState.SendUsers, text="🔙ortga")
async def exit_admin(msg: types.Message, state: FSMContext):
    await msg.answer("Orga qaytildi", reply_markup=adminButton)
    await AdminState.adminState.set()


@dp.message_handler(state=AdminState.SendGroup, text="🔙ortga")
async def exit_admin(msg: types.Message, state: FSMContext):
    await msg.answer("Orga qaytildi", reply_markup=adminButton)
    await AdminState.adminState.set()


@dp.message_handler(state=AdminState.SendUsers, content_types=types.ContentTypes.ANY)
async def send_users(msg: types.Message):
    reply_markup = msg.reply_markup
    rows = await getUserList()
    count = 0
    for row in rows:
        try:
            await msg.bot.copy_message(row.chat_id, msg.from_user.id, msg.message_id, reply_markup=reply_markup)
            count += 1
        except:
            pass
        await sleep(0.07)
    await msg.reply(f"{count} ta foydalanuvchilarga habar yuborildi")


@dp.message_handler(state=AdminState.SendGroup, content_types=types.ContentTypes.ANY)
async def send_users(msg: types.Message):
    reply_markup = msg.reply_markup
    rows = await getGroupList()
    print(rows)
    count = 0
    for row in rows:
        try:
            await msg.bot.copy_message(row.chat_id, msg.from_user.id, msg.message_id, reply_markup=reply_markup)
            count += 1
        except:
            pass

    await msg.reply(f"{count} ta Gruxlarga habar yuborildi")
