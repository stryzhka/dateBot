from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from bot.keyboards import make_keyboard, available_sex, profile_kb, static_kb, profile_kb1,  start_kb, got_match_kb
from bot.states import ProfileStates, AdminStates
from bot.misc import Bot
from aiogram import types
from bot.text.ProfileText import ProfileText
import bot.db as db
from aiogram import Router
from logger import bot_logger

router = Router()

@router.message(
    F.text == 'моя анкета',
    ProfileStates.static
)
async def my_profile(message: Message, state: FSMContext, bot: Bot):
    #if await state.get_state() == ProfileStates.static:
    #    print('static!')
    user = db.get_user(message.from_user.id)
    img = FSInputFile(user.photo)
    await message.answer_photo(
        img,
        caption = f"{user.name}, {user.sex}\n{user.description}",
        reply_markup=make_keyboard(profile_kb1)
    )
    #state.set_state(ProfileStates.in_ProfileStates)
    #print(state.get_state())

@router.message(
    ProfileStates.static,
    F.text == 'вернуться в меню'
)
@router.message(
    F.text.lower() == 'вернуться в меню',
    ProfileStates.watching 
)
@router.message(
    F.text.lower() == 'вернуться в меню',
    AdminStates.in_menu 
)
async def menu(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        text=ProfileText.MENU_TEXT(),
        reply_markup=make_keyboard(static_kb)
    )
    await state.set_state(ProfileStates.static)

@router.message(
        F.text.lower() == 'вкл выкл анкету',
        ProfileStates.static
)
async def toggle_on(message: Message, state: FSMContext, bot: Bot):
    #print(db.is_watch_toggle(message.from_user.id))
    if db.is_watch_toggle(message.from_user.id) == "True":
        db.set_watch_toggle_false(message.from_user.id)
        bot_logger.info(f'[profile] user {message.from_user.id} toggled profile off')
        await message.answer(
            text=ProfileText.PROFILE_OFF(),
            reply_markup=make_keyboard(static_kb)
        )
    else:
        db.set_watch_toggle_true(message.from_user.id)
        bot_logger.info(f'[profile] user {message.from_user.id} toggled profile on')
        await message.answer(
            text=ProfileText.PROFILE_ON(),
            reply_markup=make_keyboard(static_kb)
        )





