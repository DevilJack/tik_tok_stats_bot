from aiogram.dispatcher.filters.state import StatesGroup, State


class LoginForm(StatesGroup):
    last_message_id = State()
    tik_tok_name = State()
    tik_tok_id = State()
    role = State()
    login = State()
    password = State()
    status = State()
    chat_id = State()

class TTStatsForm(StatesGroup):
    is_sub_first = State()
    nickname = State()
    report1_is_ready = State()
    is_sub_second = State()
    file1 = State()
    file2 = State()
    