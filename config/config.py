from dataclasses import dataclass
from environs import Env


@dataclass
class TelegramBot:
    token: str


@dataclass
class Nats:
    servers: list


@dataclass
class Config:
    telegram_bot: TelegramBot
    nats: Nats


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(
        telegram_bot=TelegramBot(token=env("BOT_TOKEN")),
        nats=Nats(servers=env.list("NATS_SERVERS")),
    )

