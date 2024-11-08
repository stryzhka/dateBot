import asyncio
import sys
from logger import bot_logger, aiogram_logger
import io

from bot.config import TOKEN
from bot.misc import start_polling
from aiogram.exceptions import TelegramBadRequest
import bot.db as db

async def main() -> None:
    try:
        if sys.argv[1] is not None and sys.argv[1] == '-silence':
            bot_logger.info('started with -silence argument')
            await start_polling(silence_mode=True)
    except IndexError:
        bot_logger.info('standart start')
        await start_polling(silence_mode=False)

if __name__ == '__main__':
    asyncio.run(main())
    