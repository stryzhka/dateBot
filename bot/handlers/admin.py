import random
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F

from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from bot.keyboards import make_keyboard, available_sex, profile_kb, static_kb, profile_kb1,  start_kb, watching_kb, admin_kb
from bot.states import ProfileStates, AdminStates
from bot.misc import Bot
from aiogram import types, Dispatcher
import bot.db as db
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.storage.base import StorageKey

router = Router()

@router.message(
    F.text.lower() == "/admin",
    ProfileStates.static
)
async def open_admin_menu(message: Message, bot: Bot, state: FSMContext):
    print(db.is_user_admin(message.from_user.id))
    if db.is_user_admin(message.from_user.id):
        await state.set_state(AdminStates.in_menu)
        await message.answer(
            text="админка нефорпенза бот v66.6",
            reply_markup=make_keyboard(admin_kb)
        )
    else:
        await message.answer(
            text="ошибка доступа"
        )

@router.message(
    F.text.lower() == "сообщение всем пользователям",
    AdminStates.in_menu
)
async def message_to_all_users(message: Message, bot: Bot, state: FSMContext):
    await message.answer(
        text="введи сообщение"
    )
    await state.set_state(AdminStates.writing_msg)

@router.message(
    AdminStates.writing_msg
)
async def send_message_to_all_users(message: Message, bot: Bot, state: FSMContext):
    text = f"""
    ⚠️⚠️⚠️
    {message.text}
⚠️⚠️⚠️
    """
    for e in db.get_users_list():
        try:
            await bot.send_message(
                chat_id=e,
                text=text
            )
        except TelegramBadRequest:
            await message.answer(
                text=f'не отправилось пользователю {e}'
            )
    await state.set_state(AdminStates.in_menu)

@router.message(
    F.text.lower() == "жалобы",
    AdminStates.in_menu
)
async def start_watch_complains(message: Message, bot: Bot, state: FSMContext):
    pass