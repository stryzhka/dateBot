from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F

from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from bot.keyboards import make_keyboard, available_sex, profile_kb, static_kb, profile_kb1,  start_kb, got_match_kb
from bot.states import ProfileStates
from bot.misc import Bot
from aiogram import types
import bot.db as db
from aiogram import Router

router = Router()


@router.message(
    F.text == 'моя анкета',
    ProfileStates.static
)
async def my_profile(message: Message, state: FSMContext, bot: Bot):
    if await state.get_state() == ProfileStates.static:
        print('static!')
    user = db.get_user(message.from_user.id)

    print(user.photo)
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
async def menu(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        text="выбери действие",
        reply_markup=make_keyboard(static_kb)
    )
    await state.set_state(ProfileStates.static)

@router.message(
        F.text.lower() == 'вкл выкл анкету',
        ProfileStates.static
)
async def toggle_on(message: Message, state: FSMContext, bot: Bot):
    print(db.is_watch_toggle(message.from_user.id))
    if db.is_watch_toggle(message.from_user.id) == "True":
        db.set_watch_toggle_false(message.from_user.id)
        await message.answer(
            text="теперь твоя анкета отключена, ее не будут видеть при поиске, но ты не сможешь ставить лайки",
            reply_markup=make_keyboard(static_kb)
        )
    else:
        db.set_watch_toggle_true(message.from_user.id)
        await message.answer(
            text="теперь твоя анкета включена, ее будут видеть при поиске и ты сможешь ставить лайки",
            reply_markup=make_keyboard(static_kb)
        )

async def words_check(message: Message):
    if message.entities != None:
        for e in message.entities:
            if e.type in ['mention', 'url', 'email', 'phone_number']:
                await message.answer(
                    text='что-то пошло не так, попробуй еще раз 0_0'
                )
                return



