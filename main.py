import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import routers
from config import Config, load_config
from storage.nats_storage import NatsStorage
from utils.nats_connect import connect_to_nats
from utils.start_consumers import start_delayed_consumer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():

    logger.info("Start Bot")

    config: Config = load_config()

    nc, js = await connect_to_nats(config.nats.servers)

    storage: NatsStorage = await NatsStorage(nc=nc, js=js).create_storage()

    bot = Bot(config.telegram_bot.token)
    dp = Dispatcher(storage=storage)

    # Подключаем роутеры
    dp.include_routers(*routers())

    try:
        await asyncio.gather(
            dp.start_polling(
                bot,
                js=js,
                delay_subject=config.delayed_consumer.subject,
            ),
            start_delayed_consumer(
                nc=nc,
                js=js,
                bot=bot,
                subject=config.delayed_consumer.subject,
                stream=config.delayed_consumer.stream,
                durable_name=config.delayed_consumer.durable_name,
            ),
        )
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
