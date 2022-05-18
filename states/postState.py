from aiogram.dispatcher.filters.state import State, StatesGroup


class PostState(StatesGroup):
    moviePost = State()
    movieState = State()
    movieLangState = State()
    moviePicks = State()
    movieGenre = State()
    movieCode = State()
