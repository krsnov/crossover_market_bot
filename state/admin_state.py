from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    number = State()
    add = State()
    minus = State()
    get_admin = State()
    bonus = State()
    set_bonus = State()
    picture = State()
    msg = State()
    _pass = State()
