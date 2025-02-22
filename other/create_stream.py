import asyncio

from nats.js.api import DiscardPolicy, RetentionPolicy, StorageType, StreamConfig
from config import Config, load_config
from utils.nats_connect import connect_to_nats


async def create_stream():

    config: Config = load_config()
    _, js = await connect_to_nats(config.nats.servers)

    await js.add_stream(
        StreamConfig(
            name=config.delayed_consumer.stream,
            subjects=[config.delayed_consumer.subject],
            storage=StorageType.FILE,
            discard=DiscardPolicy.OLD,
            retention=RetentionPolicy.LIMITS,
            num_replicas=1,
            duplicate_window=2.0,
        )
    )



asyncio.run(create_stream())
