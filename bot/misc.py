from aiogram import Bot, Dispatcher, types
from bot.config import TOKEN
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers import profile, watch, matches, registering, admin, bot_condition
from aiogram.exceptions import TelegramForbiddenError
import asyncio


bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
async def start_polling(silence_mode=False):
    try:
        if silence_mode:
            dp.include_routers(profile.router, watch.router, matches.router, registering.router, admin.router)
        else:
            dp.include_routers(profile.router, watch.router, matches.router, registering.router, admin.router, bot_condition.router)
        
    except TelegramForbiddenError:
        pass
    await dp.start_polling(bot)
    
