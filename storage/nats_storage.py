from typing import Any, Dict, Self
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    KeyBuilder,
    DefaultKeyBuilder,
    StorageKey,
)
from nats.aio.client import Client
from nats.js import JetStreamContext
from nats.js.api import KeyValueConfig, StorageType
from nats.js.errors import NotFoundError
from nats.js.kv import KeyValue
import ormsgpack


class NatsStorage(BaseStorage):

    def __init__(
        self,
        nc: Client,
        js: JetStreamContext,
        key_builder: KeyBuilder | None = None,
        fsm_states_bucket: str = "fsm_states_aiogram",
        fsm_data_bucket: str = "fsm_data_aiogram",
    ) -> None:

        if key_builder is None:
            key_builder = DefaultKeyBuilder()

        self.nc = nc
        self.js = js
        self._key_builder = key_builder
        self.fsm_states_bucket = fsm_states_bucket
        self.fsm_data_bucket = fsm_data_bucket

    async def create_storage(self) -> Self:
        self.kv_states = await self._get_kv_states()
        self.kv_data = await self._get_kv_data()
        return self

    async def _get_kv_states(self) -> KeyValue:
        config = KeyValueConfig(
            bucket=self.fsm_states_bucket,
            history=5,
            storage=StorageType.FILE,
        )
        return await self.js.create_key_value(config=config)

    async def _get_kv_data(self) -> KeyValue:
        config = KeyValueConfig(
            bucket=self.fsm_data_bucket,
            history=5,
            storage=StorageType.FILE,
        )
        return await self.js.create_key_value(config=config)

    async def set_state(
        self, key: StorageKey, state: str | State | None = None
    ) -> None:
        state = state.state if isinstance(state, State) else state
        await self.kv_states.put(
            key=self._key_builder.build(key), value=ormsgpack.packb(state or None)
        )

    async def get_state(self, key: StorageKey) -> str | None:
        try:
            entry = await self.kv_states.get(key=self._key_builder.build(key))
            data = ormsgpack.unpackb(entry.value)
        except NotFoundError:
            return None
        return data

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        await self.kv_data.put(
            key=self._key_builder.build(key), value=ormsgpack.packb(data)
        )

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        try:
            entry = await self.kv_data.get(key=self._key_builder.build(key))
            return ormsgpack.unpackb(entry.value)
        except NotFoundError:
            return {}

    async def close(self) -> None:
        await self.nc.close()
