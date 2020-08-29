# mypy: ignore-errors
from __future__ import annotations
from google.cloud.firestore_v1 import AsyncDocumentReference
from typing import Dict, TYPE_CHECKING, Union, Any

if TYPE_CHECKING:
    from lib import FireStore


class GuildDictSnapshot:
    def __init__(self, document: AsyncDocumentReference, guild_dict: GuildDict) -> None:
        self.document = document
        self.executor = guild_dict.executor
        self.guild_dict = guild_dict
        self.bot = guild_dict.bot

    async def data(self) -> Dict[str, str]:
        result = await self.document.get()
        d = result.to_dict()
        if d is None:
            await self.add('bard', 'バード')
            return {'bard': 'バード'}

        return d

    async def exists(self) -> bool:
        result = await self.document.get()

        return result.exists

    async def add(self, key: str, value: str) -> None:
        await self.document.set({key: value}, merge=True)

    async def remove(self, key: str) -> Any:
        base_data = await self.data()
        if key not in base_data.keys():
            return False
        del base_data[key]

        return await self.document.set(base_data)


class GuildDict:
    def __init__(self, firestore: 'FireStore'):
        self.bot = firestore.bot
        self.firestore = firestore
        self.db = firestore.db
        self.executor = firestore.executor
        self.collection = self.db.collection('guild_dict')

    def get(self, guild_id: Union[int, str]) -> GuildDictSnapshot:
        return GuildDictSnapshot(self.collection.document(str(guild_id)), self)
