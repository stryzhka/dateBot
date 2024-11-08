import asyncio
import sys
import logging
import io

from bot.config import TOKEN
from bot.misc import start_polling
from aiogram.exceptions import TelegramBadRequest
import bot.db as db
#from bot.handlers.bot_condition import on_startup, on_shutdown

#def on_startup():
#    print("ХУЙ")
    

async def main() -> None:
    try:
        if sys.argv[1] is not None and sys.argv[1] == '-silence':
            print('-silence argument')
            await start_polling(silence_mode=True)
    except IndexError:
        print('no argument')
        await start_polling(silence_mode=False)

if __name__ == '__main__':
    
    
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    