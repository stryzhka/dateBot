import random
from aiogram.filters import CommandObject
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F

from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from bot.keyboards import make_keyboard, available_sex, profile_kb, static_kb, profile_kb1,  start_kb, watching_kb, admin_kb, banlist_kb
from bot.states import ProfileStates, AdminStates
from bot.misc import Bot
from aiogram import types, Dispatcher
import bot.db as db
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.fsm.storage.base import StorageKey
from bot.text.AdminText import AdminText
from logger import bot_logger

router = Router()

@router.message(
    F.text.lower() == "/admin",
    ProfileStates.static
)
async def open_admin_menu(message: Message, bot: Bot, state: FSMContext):
    bot_logger.warning(f'[admin] {message.from_user.id} trying to admin...')
    if db.is_user_admin(message.from_user.id):
        await state.set_state(AdminStates.in_menu)
        await message.answer(
            text=AdminText.START(),
            reply_markup=make_keyboard(admin_kb)
        )
        bot_logger.warning(f'[admin] {message.from_user.id} entered admin')
    else:
        await message.answer(
            text=AdminText.FAIL()
        )
        bot_logger.warning(f'[admin] {message.from_user.id} failed admin')

@router.message(
    F.text.lower() == "сообщение всем пользователям",
    AdminStates.in_menu
)
async def message_to_all_users(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        text=AdminText.INPUT()
    )
    await state.set_state(AdminStates.writing_msg)

@router.message(
    AdminStates.writing_msg
)
async def send_message_to_all_users(message: Message, bot: Bot, state: FSMContext):
    text = AdminText.MSG_TO_ALL(message.text)
    for e in db.get_users_list():
        try:
            await bot.send_message(
                chat_id=e,
                text=text
            )
        except TelegramBadRequest:
            await message.answer(
                text=AdminText.SEND_FAIL(e)
            )
            bot_logger.warning(f'[admin] failed to send to {e}')
        except TelegramForbiddenError:
            await message.answer(
                text=AdminText.SEND_FAIL(e)
            )
            bot_logger.warning(f'[admin] failed to send to {e}')
    await state.set_state(AdminStates.in_menu)

@router.message(
    F.text.lower() == "жалобы",
    AdminStates.in_menu
)
async def start_watch_complain(message: Message, state: FSMContext, bot: Bot):
    l = db.get_complains()
    if (len(l) > 0):
        await state.update_data(
            complain_index=0
        )
        data = await state.get_data()
        img = FSInputFile(l[data['complain_index']].photo)
        await message.answer_photo(
            img,
            caption = f"{l[data['complain_index']].name}, {l[data['complain_index']].username}, {l[data['complain_index']].user_id}",
            reply_markup=make_keyboard(banlist_kb)
        )
        await state.set_state(AdminStates.watching_complains)
    else:
        await message.answer(
        text=AdminText.COMPLAINS_END()
    )    


@router.message(
    F.text.lower() == 'далее',
    AdminStates.watching_complains
)
async def next_complain(message: Message, state: FSMContext, bot: Bot):
    l = db.get_complains()
    data = await state.get_data()
    await state.update_data(
            complain_index=data['complain_index'] + 1
        )
    data = await state.get_data()
    if data['complain_index']  == len(l):
        await message.answer(
            text=AdminText.COMPLAINS_END(),
            reply_markup=make_keyboard(admin_kb)
        )
        await state.set_state(AdminStates.in_menu)
    else:
        img = FSInputFile(l[data['complain_index']].photo)
        await message.answer_photo(
            img,
            caption = f"{l[data['complain_index']].name}, {l[data['complain_index']].username}, {l[data['complain_index']].user_id}",
            reply_markup=make_keyboard(banlist_kb)
        )
    
@router.message(
    F.text.lower() == 'выйти',
    AdminStates.watching_complains
)
async def exit(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(AdminStates.in_menu)
    await open_admin_menu(message, bot, state)

@router.message(
    F.text.lower() == 'черный список',
    AdminStates.in_menu
)
async def blacklist(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        text=str(db.get_blacklist())
    )

@router.message(
        Command('ban'),
        AdminStates.in_menu
        )
async def ban(message: Message, bot: Bot, state: FSMContext, command: CommandObject):
    args = command.args
    #print(type(args))
    if args is None:
        await message.answer(
            text='ошибка'
        )
        bot_logger.warning(f'[admin] {message.from_user.id} failed to ban')
        return
    if args is not args.isspace():
        if db.blacklist_exist(int(args)):
            await message.answer(
                text=AdminText.ALREADY_BANNED()
            )
        else:
            '''if db.complain_exists(int(args)):
                await message.answer(
                    text=AdminText.BANNED()
                )
                db.remove_complain(int(args))
                db.add_to_blacklist(int(args))
                await bot.send_message(
                    chat_id=int(args),
                    text=AdminText.GOT_BAN()
                )
            else:
                await message.answer(
                    text=AdminText.NO_COMPLAINS()
                )'''
            try:
                if db.exist(int(args)):
                    await message.answer(
                        text=AdminText.BANNED()
                    )
                    if db.complain_exists(int(args)):
                        db.remove_complain(int(args))
                    db.add_to_blacklist(int(args))
                    await bot.send_message(
                        chat_id=int(args),
                        text=AdminText.GOT_BAN()
                    )
                    bot_logger.warning(f'[admin] {message.from_user.id} banned {args}')
                else:
                    await message.answer(
                        text=AdminText.ERROR()
                    )
                    bot_logger.warning(f'[admin] {message.from_user.id} failed to ban')
            except TelegramForbiddenError:
                await message.answer(
                        text=AdminText.ERROR()
                    )
                bot_logger.warning(f'[admin] user {args} is unreachable')
    else:
        await message.answer(
            text=AdminText.ERROR()
        )
        bot_logger.warning(f'[admin] {message.from_user.id} failed to ban')

@router.message(
        Command('unban'),
        AdminStates.in_menu
        )
async def unban(message: Message, bot: Bot, state: FSMContext, command: CommandObject):
    args = command.args
    if args is None:
        await message.answer(
            text=AdminText.ERROR()
        )
        return
    if args is not args.isspace():
        if db.blacklist_exist(int(args)):
            try:
                await message.answer(
                    text=AdminText.UNBANNED()
                )
                await bot.send_message(
                    chat_id=int(args),
                    text=AdminText.GOT_UNBAN()
                )
                db.remove_from_blacklist(int(args))
                bot_logger.warning(f'[admin] {message.from_user.id} unbanned {args}')
            except TelegramForbiddenError:
                await message.answer(
                        text=AdminText.ERROR()
                    )
                bot_logger.warning(f'[admin] user {args} is unreachable')
                
        else:
            await message.answer(
                text=AdminText.NOT_BANNED()
            )
    else:
        await message.answer(
            text=AdminText.ERROR()
        )
        bot_logger.warning(f'[admin] {message.from_user.id} failed to unban')

@router.message(
        Command('clean'),
        AdminStates.in_menu
        )
async def clean_complains(message: Message, bot: Bot, state: FSMContext, command: CommandObject):
    db.clean_complains()
    await message.answer(
        text=AdminText.COMPLAINS_CLEAN()
    )
    bot_logger.warning(f'[admin] {message.from_user.id} cleaned complains')

@router.message(
    Command('assign'),
    AdminStates.in_menu
)
async def assign(message: Message, bot: Bot, state: FSMContext, command: CommandObject):
    args = command.args
    if args is None:
        await message.answer(
            text=AdminText.ERROR()
        )
        return
    if args is not args.isspace():
        if db.exist(int(args)):
            try:
                if int(args) == message.from_user.id:
                    await message.answer(
                        text=AdminText.ERROR()
                    )
                    return
                await message.answer(
                    text=AdminText.ADMIN_ADDED()
                )
                await bot.send_message(
                    chat_id=int(args),
                    text=AdminText.GOT_ADMIN()
                )
                bot_logger.warning(f'[admin] {message.from_user.id} assigned {args} as admin')
            except TelegramForbiddenError:
                await message.answer(
                        text=AdminText.ERROR()
                    )
                bot_logger.warning(f'[admin] user {args} is unreachable')
        else:
            await message.answer(
                text=AdminText.ERROR()
            )
    else:
        await message.answer(
            text=AdminText.ERROR()
        )
        bot_logger.warning(f'[admin] {message.from_user.id} failed to assign')

@router.message(
    Command('unassign'),
    AdminStates.in_menu
)
async def assign(message: Message, bot: Bot, state: FSMContext, command: CommandObject):
    args = command.args
    if args is None:
        await message.answer(
            text=AdminText.ERROR()
        )
        return
    if args is not args.isspace():
        if db.admin_exist(int(args)):
            try:
                if int(args) == message.from_user.id:
                    await message.answer(
                        text=AdminText.ERROR()
                    )
                    return
                await message.answer(
                    text=AdminText.ADMIN_DELETED()
                )
                await bot.send_message(
                    chat_id=int(args),
                    text=AdminText.GOT_UNASSIGN()
                )
                bot_logger.warning(f'[admin] {message.from_user.id} unassigned {args}')
            except:
                await message.answer(
                        text=AdminText.ERROR()
                    )
                bot_logger.warning(f'[admin] user {args} is unreachable')
        else:
            await message.answer(
                text=AdminText.ERROR()
            )
    else:
        await message.answer(
            text=AdminText.ERROR()
        )
        bot_logger.warning(f'[admin] {message.from_user.id} failed to unassign')