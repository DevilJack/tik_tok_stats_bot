from aiogram.dispatcher.filters.state import StatesGroup, State


class TTStatsForm(StatesGroup):
    is_sub_first = State()
    nickname = State()
    report1_is_ready = State()
    is_sub_second = State()
    file1 = State()
    file2 = State()
    