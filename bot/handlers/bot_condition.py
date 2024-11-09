from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from bot.keyboards import make_keyboard, available_sex, profile_kb, static_kb, profile_kb1,  start_kb, got_match_kb
from bot.states import ProfileStates
from bot.misc import Bot
from aiogram import types
import bot.db as db
from aiogram import Router
from bot.text.MatchesText import MatchesText
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

router = Router()

@router.startup()
async def on_startup(bot: Bot):
    await bot.session.close()
    text = 'НЕФОРПЕНЗАБОТ АКТИВИРОВАН\nпропишите /start'
    for e in db.get_users_list():
        try:
            await bot.send_message(
                chat_id=e,
                text=text
            )
        except TelegramBadRequest:
            print('cant send request')
        except TelegramForbiddenError:
            print('cant send request')
    

@router.shutdown()
async def on_shutdown(bot: Bot):
    await bot.session.close()
    text = 'НЕФОРПЕНЗАБОТ ВЫКЛЮЧАЕТСЯ...'
    for e in db.get_users_list():
        try:
            await bot.send_message(
                chat_id=e,
                text=text
            )
        except TelegramBadRequest:
            await bot.session.close()
            print('cant send request')
        except TelegramForbiddenError:
            print('cant send request')
    
