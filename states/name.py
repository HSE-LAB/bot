from aiogram.dispatcher.filters.state import State, StatesGroup


class UserName(StatesGroup):
    name = State()
    changed_name = State()

    num_settings = State()
    num = State()
    changed_num = State()

    addr_settings = State()
    address = State()
    changed_address = State()


    fillin_db = State()
