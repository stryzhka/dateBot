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