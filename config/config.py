from dataclasses import dataclass
from environs import Env


@dataclass
class TelegramBot:
    token: str


@dataclass
class Nats:
    servers: list


@dataclass
class NatsDelayedConsumerConfig:
    subject: str
    stream: str
    durable_name: str


@dataclass
class Config:
    telegram_bot: TelegramBot
    nats: Nats
    delayed_consumer: NatsDelayedConsumerConfig


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(
        telegram_bot=TelegramBot(token=env("BOT_TOKEN")),
        nats=Nats(servers=env.list("NATS_SERVERS")),
        delayed_consumer=NatsDelayedConsumerConfig(
            subject=env("NATS_DELAYED_CONSUMER_SUBJECT"),
            stream=env("NATS_DELAYED_CONSUMER_STREAM"),
            durable_name=env("NATS_DELAYED_CONSUMER_DURABLE_NAME"),
        ),
    )
