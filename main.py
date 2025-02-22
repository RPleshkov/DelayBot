import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import Config, load_config
from storage.nats_storage import NatsStorage
from utils.nats_connect import connect_to_nats

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():

    logger.info("Start Bot")

    config: Config = load_config()

    nc, js = await connect_to_nats(config.nats.servers)

    storage: NatsStorage = await NatsStorage(nc=nc, js=js).create_storage()

    bot = Bot(config.telegram_bot.token)
    dp = Dispatcher(storage=storage)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
        logger.info("Connection to NATS closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stop Bot")
