from aiogram.fsm.state import StatesGroup, State


class AddTgAccState(StatesGroup):
    input_number = State()
    input_2fa = State()
    input_code = State()


class DelTgAccState(StatesGroup):
    input_number = State()
    update_db = State()


class AddGroup(StatesGroup):
    input_group = State()


class DelGroup(StatesGroup):
    input_group = State()


class EditPromts(StatesGroup):
    edit_promt = State()

class Triggers(StatesGroup):
    add_trigger = State()
    del_trigger = State()

class AddGPTAccState(StatesGroup):
    input_api = State()

class DelGPTState(StatesGroup):
    input_key = State()

class UsersAddState(StatesGroup):
    input_creds = State()

class UsersDelState(StatesGroup):
    input_id = State()

class PromoteUser(StatesGroup):
    input_promote = State()

class TranferAcc(StatesGroup):
    input_acc = State()

class EditAccInfo(StatesGroup):
    change_name = State()
    change_surname = State()
    change_bio = State()
