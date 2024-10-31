from aiogram.fsm.state import StatesGroup, State
class ProfileStates(StatesGroup):
    setup = State()
    choosing_sex = State()
    choosing_name = State()
    choosing_description = State()
    choosing_photo = State()
    static = State()
    profile_ended = State()
    in_profile = State()
    watching = State()
    watching_matches = State()

class AdminStates(StatesGroup):
    in_menu = State()
    writing_msg = State()
    watching_complains = State()