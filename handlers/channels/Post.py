import os
import re
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.default.adminKeyboard import adminButton, back
from keyboards.default.postKeyboard import postLangKeyboard
from keyboards.inline.addInline import addButtonsInline, bekorqilish, addLimitButtonsInline
from keyboards.inline.delInline import submitInline
from loader import dp
from states.adminState import AdminState, AddState
from states.postState import PostState
from utils.db_api.model import getUserList, getUsersCount, getGroupList, getGroupsCount, new_movie_add
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(commands="post")
async def postChanel(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    if str(user_id) in ADMINS:
        await msg.reply("Salom Xurmatli admin \n\nKanalga post joylash uchun rasm yuboring!")
        await PostState.moviePost.set()
        return
    if os.stat("data/admin/admin.txt").st_size == 0:
        await msg.reply("<b>Siz noto'g'ri buyruq kiritdingiz!</b>")
        return
    f = open('data/admin/admin.txt', 'r')
    read = f.read()
    read = read.split('\n')
    f.close()
    if str(user_id) in read:
        await msg.reply("Salom Xurmatli admin \n\nKanalga post joylash uchun rasm yuboring!")
        await PostState.moviePost.set()
    else:
        await msg.reply("<b>Siz noto'g'ri buyruq kiritdingiz!</b>")


@dp.message_handler(state=PostState.moviePost, content_types=types.ContentTypes.PHOTO)
async def postPhoto(msg: types.Message, state: FSMContext):
    photo_id = msg.photo[-1].file_id
    await state.update_data({
        "photo": photo_id
    })
    await msg.answer("<b>Kino nomini kiriting:</b>")
    await PostState.movieState.set()


@dp.message_handler(state=PostState.movieState, content_types=types.ContentTypes.TEXT)
async def name(msg: types.Message, state: FSMContext):
    movie_name = msg.text
    await state.update_data({
        "movie_name": movie_name
    })
    await msg.answer("<b>Kino tilini kiriting:</b>", reply_markup=postLangKeyboard)
    await PostState.movieLangState.set()


@dp.message_handler(state=PostState.movieLangState, content_types=types.ContentTypes.TEXT)
async def quality(msg: types.Message, state: FSMContext):
    movie_lang = msg.text
    await state.update_data({
        "movie_lang": movie_lang
    })
    await msg.answer("<b>Kino Sifatini kiriting:</b>", reply_markup=ReplyKeyboardRemove())
    await PostState.moviePicks.set()


@dp.message_handler(state=PostState.moviePicks, content_types=types.ContentTypes.TEXT)
async def genre(msg: types.Message, state: FSMContext):
    movie_pick = msg.text
    await state.update_data({
        "movie_pick": movie_pick
    })
    await msg.answer("<b>Kino Janrini kiriting:</b>")
    await PostState.movieGenre.set()


@dp.message_handler(state=PostState.movieGenre, content_types=types.ContentTypes.TEXT)
async def finish(msg: types.Message, state: FSMContext):
    movie_genre = msg.text
    await state.update_data({
        "movie_genre": movie_genre
    })
    await msg.answer("<b>Kino kodini kiriting:</b>")
    await PostState.movieCode.set()


@dp.message_handler(state=PostState.movieCode, content_types=types.ContentTypes.TEXT)
async def finish(msg: types.Message, state: FSMContext):
    movie_code = msg.text
    await state.update_data({
        "movie_code": movie_code
    })
    data = await state.get_data()
    photo_id = data.get("photo")
    movie_name = data.get("movie_name")
    movie_lang = data.get("movie_lang")
    movie_pick = data.get("movie_pick")
    movie_genre = data.get("movie_genre")
    movie_code = data.get("movie_code")
    captions = f"<b>📹Kino nomi: {movie_name}\n➖➖➖➖➖➖➖➖➖➖\n\n{movie_lang}\n🖥Sifati: {movie_pick}\n📽Janri: {movie_genre}\n\nKino  @KinoYukladiBot ga joylandi!\n✅KINO KODI👉: {movie_code}</b>"
    await msg.answer_photo(photo=photo_id, caption=captions, reply_markup=submitInline)


@dp.callback_query_handler(state=PostState.movieCode, text="send")
async def sendPost(msg: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photo_id = data.get("photo")
    movie_name = data.get("movie_name")
    movie_lang = data.get("movie_lang")
    movie_pick = data.get("movie_pick")
    movie_genre = data.get("movie_genre")
    movie_code = data.get("movie_code")
    captions = f"<b>📹Kino nomi: {movie_name}\n➖➖➖➖➖➖➖➖➖➖\n\n{movie_lang}\n🖥Sifati: {movie_pick}\n📽Janri: {movie_genre}\n\nKino  @KinoYukladiBot ga joylandi!\n✅KINO KODI👉: {movie_code}</b>"
    await msg.bot.send_photo(chat_id=-1001500212814, photo=photo_id, caption=captions, reply_markup=submitInline)
    await msg.message.answer("Post yuborildi!")
    await state.finish()


@dp.callback_query_handler(state=PostState.movieCode, text="cansel")
async def cancel(msg: types.CallbackQuery, state: FSMContext):
    await msg.message.answer("Bekor qilindi!")
    await state.finish()
