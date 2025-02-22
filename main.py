import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import Config, load_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():

    logger.info("Start Bot")

    config: Config = load_config()

    bot = Bot(config.telegram_bot.token)
    dp = Dispatcher()

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stop Bot")
