# mypy: ignore-errors
from __future__ import annotations
from google.cloud.firestore_v1 import Increment, AsyncDocumentReference
from typing import Dict, Optional, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from lib import FireStore


class GuildData:
    def __init__(self, data: Dict[str, int]) -> None:
        self.data = data

    @property
    def count(self) -> int:
        return sum(value for key, value in self.data.items() if key != 'subscribe')

    @property
    def subscribe(self) -> int:
        return self.data['subscribe']

    def is_spendable(self, count: int) -> bool:
        return self.count - count >= 0


class GuildSnapshot:
    def __init__(self, document: AsyncDocumentReference, guild: Guild):
        self.document = document
        self.guild = guild
        self.executor = guild.executor
        self.bot = guild.bot

    async def data(self) -> GuildData:
        result = await self.document.get()

        return GuildData(result.to_dict())

    async def exists(self) -> bool:
        result = await self.document.get()

        return result.exists

    async def set(self, count: int) -> None:
        await self.document.set({'count': count}, merge=True)

    async def create(self) -> Optional[GuildData]:
        """TODO: GuildにBotが入った時に実行する"""
        if await self.exists():
            return
        payload = dict(subscribe=0, count=3000)

        await self.document.set(payload)
        return GuildData(payload)

    async def spend_char(self, count: int) -> None:
        """使用可能文字数を減らす"""
        data = await self.data()
        data2 = {key: value for key, value in data.data.items() if key != 'subscribe' and value != 0}
        used_data = {}
        if not data2:
            return
        while count > 0:
            min_key = min(data2, key=data2.get)
            if count > data2[min_key]:
                count -= data2[min_key]
                used_data[min_key] = 0
                del data2[min_key]
                continue
            used_data[min_key] = Increment(-count)
            count = 0
        await self.document.set(used_data, merge=True)

    async def set_data(self, new_data: Dict[str, int]):
        await self.document.set(new_data, merge=True)

    async def set_subscribe(self) -> None:
        await self.document.set({'subscribe': 1}, merge=True)


class Guild:
    def __init__(self, firestore: 'FireStore'):
        self.bot = firestore.bot
        self.firestore = firestore
        self.db = firestore.db
        self.executor = firestore.executor
        self.collection = self.db.collection('guilds')

    def get(self, guild_id: Union[int, str]) -> GuildSnapshot:
        return GuildSnapshot(self.collection.document(str(guild_id)), self)
