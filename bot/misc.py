from aiogram import Bot, Dispatcher, types
from bot.config import TOKEN
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers import profile, watch, matches, registering, admin


bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_routers(profile.router, watch.router, matches.router, registering.router, admin.router)

