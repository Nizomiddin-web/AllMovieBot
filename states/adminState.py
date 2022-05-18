from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminState(StatesGroup):
    adminState = State()
    SendUsers = State()
    SendGroup = State()


class AddState(StatesGroup):
    addChanelState = State()
    addAdminState = State()
    addMovieState = State()
    delChanel = State()