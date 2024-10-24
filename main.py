import asyncio
import sys
import logging
import io

from bot.config import TOKEN
from bot.misc import dp, bot




async def main() -> None:
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())