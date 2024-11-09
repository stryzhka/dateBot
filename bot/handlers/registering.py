from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import F

from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from bot.keyboards import make_keyboard, available_sex, profile_kb, static_kb, profile_kb1,  start_kb, got_match_kb
from bot.states import ProfileStates
from bot.misc import Bot
from aiogram import types
import bot.db as db
from aiogram import Router
from bot.text.RegisteringText import RegisteringText
from logger import bot_logger

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if db.exist(message.from_user.id):
        await message.answer(RegisteringText.START_HAS_PROFILE(), reply_markup=make_keyboard(static_kb))
        await state.set_state(ProfileStates.static)
        bot_logger.info(f'[registering] registered user {message.from_user.username} {message.from_user.id} started')
    else:
        await message.answer(RegisteringText.START_NO_PROFILE(message.from_user.full_name), reply_markup=make_keyboard(start_kb))
        await state.set_state(ProfileStates.setup)
        bot_logger.info(f'[registering] new user {message.from_user.username} {message.from_user.id} started')

@router.message(
    F.text.lower() == 'создать анкету',
    ProfileStates.setup
)
@router.message(F.text.lower() == 'изменить анкету', ProfileStates.profile_ended)
@router.message(F.text.lower() == 'изменить анкету', ProfileStates.static)
async def create_profile_begin(message: types.Message, state: FSMContext):
    await message.reply(RegisteringText.CHOOSE_NAME(), reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ProfileStates.choosing_name)

@router.message(
    ProfileStates.choosing_name
)
async def create_profile_sex(message: Message, state: FSMContext):
    if await words_check(message):
        await state.update_data(name=message.text)
        await message.answer(
            text=RegisteringText.CHOOSE_SEX(),
            reply_markup=make_keyboard(available_sex)
        )
        await state.set_state(ProfileStates.choosing_sex)

@router.message(
    ProfileStates.choosing_sex,
    F.text.in_(available_sex)
)
async def create_profile_description(message: Message, state: FSMContext):
    await state.update_data(
        sex=message.text
    )
    await message.answer(
        text=RegisteringText.CHOOSE_DESCRIPTION(),
        reply_markup = types.ReplyKeyboardRemove()
    )
    await state.set_state(ProfileStates.choosing_description)

@router.message(
    ProfileStates.choosing_description,
    F.text.len() > 128
)
async def create_profile_description_fail(message: Message, state: FSMContext):
    await message.answer(
        text=RegisteringText.CHOOSE_DESCRIPTION_FAIL(),
    )
    await state.set_state(ProfileStates.choosing_description)

@router.message(
    ProfileStates.choosing_description,
    F.text.len() <= 128
)
async def create_profile_photo(message: Message, state: FSMContext):
    if await words_check(message):
        await state.update_data(
            description=message.text
        )
        await message.answer(
            text=RegisteringText.CHOOSE_PHOTO()
        )
        await state.set_state(ProfileStates.choosing_photo)

@router.message(
    ProfileStates.choosing_photo,
    F.photo
)
async def profile_finished(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.update_data(photo=message.photo[-1])
    data = await state.get_data()
    _desc = f"{data['name']}, {data['sex']}\n{data['description']}"

    await message.answer_photo(
        message.photo[-1].file_id,
        caption=_desc
    )

    await message.answer(
        text=RegisteringText.PROFILE_SAVE(),
        reply_markup=make_keyboard(profile_kb)
    )
    await state.set_state(ProfileStates.profile_ended)

@router.message(
    ProfileStates.profile_ended,
    F.text == 'сохранить анкету'
)
async def profile_save(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photo_path = f"photos/{data['photo_id']}.jpg"
    #print(photo_path)
    await bot.download(
        data['photo'],
        destination=photo_path
    )
    if db.exist(message.from_user.id):
        db.update_user(message.from_user.id, data['name'], data['sex'], data['description'], photo_path)
        bot_logger.info(f'[registering] user {message.from_user.id} {message.from_user.username} updated')
    else:
        db.add_user(message.from_user.id, message.from_user.username, data['name'], data['sex'], data['description'], photo_path)
        bot_logger.info(f'[registering] user {message.from_user.id} {message.from_user.username} registered')
    await message.answer(
        text=RegisteringText.PROFILE_READY(),
        reply_markup=make_keyboard(static_kb)
    )
    await state.set_state(ProfileStates.static)
    

async def words_check(message: Message):
    
    if message.entities != None:
        for e in message.entities:
            if e.type in ['mention', 'url', 'email', 'phone_number']:
                await message.answer(
                    text=RegisteringText.FAIL()
                )
                return False
    return True
