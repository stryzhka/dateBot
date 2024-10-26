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

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if db.exist(message.from_user.id):
        await message.answer(f'у тебя уже есть анкета', reply_markup=make_keyboard(static_kb))
        await state.set_state(ProfileStates.static)
    else:
        await message.answer(f'привет, {hbold(message.from_user.full_name)}\n, создай анкету', reply_markup=make_keyboard(start_kb))
        #db.add_user(message.from_user.id, message.from_user.username)
        await state.set_state(ProfileStates.setup)

@router.message(
    F.text.lower() == 'создать анкету',
    ProfileStates.setup
)
@router.message(F.text.lower() == 'изменить анкету', ProfileStates.profile_ended)
@router.message(F.text.lower() == 'изменить анкету', ProfileStates.static)
async def create_profile_begin(message: types.Message, state: FSMContext):
    await message.reply('введи свое имя (ну или что-нибудь смешное хз)', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ProfileStates.choosing_name)

@router.message(
    ProfileStates.choosing_name
)
async def create_profile_sex(message: Message, state: FSMContext):
    print(message.entities)
    if message.entities != None:
        for e in message.entities:
            if e.type in ['mention', 'url', 'email', 'phone_number']:
                await message.answer(
                    text='что-то пошло не так, попробуй еще раз 0_0'
                )
                return
        
    await state.update_data(name=message.text)
    await message.answer(
        text='теперь выбери свой гендер или пол или как там это называется',
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
        text='напиши описание - чем любишь заниматься, любимые группы, увлечения, все такое',
        reply_markup = types.ReplyKeyboardRemove()
    )
    await state.set_state(ProfileStates.choosing_description)

@router.message(
    ProfileStates.choosing_description,
    F.text.len() > 128
)
async def create_profile_description_fail(message: Message, state: FSMContext):
    await message.answer(
        text='описание слишком длинное! попробуй сократить, максимум - 128 символов',
    )
    await state.set_state(ProfileStates.choosing_description)

@router.message(
    ProfileStates.choosing_description,
    F.text.len() <= 128
)
async def create_profile_photo(message: Message, state: FSMContext):
    if message.entities != None:
        for e in message.entities:
            if e.type in ['mention', 'url', 'email', 'phone_number']:
                await message.answer(
                    text='что-то пошло не так, попробуй еще раз 0_0'
                )
                return
    await state.update_data(
        description=message.text
    )
    await message.answer(
        text='скинь фотку для анкеты',
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
        text='анкета готова! теперь сохрани ее',
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
    print(photo_path)
    await bot.download(
        data['photo'],
        destination=photo_path
    )
    db.add_user(message.from_user.id, message.from_user.username, data['name'], data['sex'], data['description'], photo_path)
    await message.answer(
        text='анкета сохранена',
        reply_markup=make_keyboard(static_kb)
    )
    await state.set_state(ProfileStates.static)

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

async def words_check(message: Message):
    if message.entities != None:
        for e in message.entities:
            if e.type in ['mention', 'url', 'email', 'phone_number']:
                await message.answer(
                    text='что-то пошло не так, попробуй еще раз 0_0'
                )
                return

@router.message(
    F.text.lower() == 'симпатии',
    ProfileStates.static
)
async def start_watch_matches(message: Message, state: FSMContext, bot: Bot):
    l = db.get_matches(message.from_user.id)
    print(l)
    if (len(l) > 0):
        await state.update_data(
            match_index=0
        )
        data = await state.get_data()
        img = FSInputFile(l[data['match_index']].photo)
        await message.answer_photo(
            img,
            caption = f"{l[data['match_index']].name}, {l[data['match_index']].sex}\n{l[data['match_index']].description}",
            reply_markup=make_keyboard(got_match_kb)
        )
        await state.set_state(ProfileStates.watching_matches)
    else:
        await message.answer(
        text="нет симпатий :("
    )
        
@router.message(
    F.text.lower() == '<3',
    ProfileStates.watching_matches
)
async def match_like(message: Message, state: FSMContext, bot: Bot):
    l = db.get_matches(message.from_user.id)
    data = await state.get_data()
    print(l[data['match_index']].username)
    await message.answer(
        text=f'@{l[data['match_index']].username} начинай общаться!'
    )
    await bot.send_message(
        chat_id=l[data['match_index']].user_id,
        text=f'на твою симпатию ответил @{db.get_user(message.from_user.id).username}, начинай общаться!'
    )

    db.remove_match(l[data['match_index']].user_id, message.from_user.id)
    print("index", data['match_index'])
    print("len", len(l))
    if data['match_index'] + 1 >= len(l):
        await message.answer(
            text='больше нет симпатий',
            reply_markup=make_keyboard(static_kb)
        )
        await state.set_state(ProfileStates.static)
    else:
        await state.update_data(
            match_index=data['match_index'] + 1
        )
        data = await state.get_data()
        img = FSInputFile(l[data['match_index']].photo)
        await message.answer_photo(
            img,
            caption = f"{l[data['match_index']].name}, {l[data['match_index']].sex}\n{l[data['match_index']].description}",
            reply_markup=make_keyboard(got_match_kb)
        )

    

