# mypy: ignore-errors
from __future__ import annotations
from google.cloud.firestore_v1 import AsyncDocumentReference
from typing import Dict, TYPE_CHECKING, Union, Optional

if TYPE_CHECKING:
    from lib import FireStore


class SettingData:
    def __init__(self, data: Dict[str, Union[bool, int]]) -> None:
        self.data = data

    @property
    def name(self) -> bool:
        return self.data['name']

    @property
    def emoji(self) -> bool:
        return self.data['emoji']

    @property
    def bot(self) -> bool:
        return self.data['bot']

    @property
    def limit(self) -> int:
        return self.data['limit']

    @property
    def keep(self) -> bool:
        return self.data['keep']


class SettingSnapshot:
    def __init__(self, document: AsyncDocumentReference, setting: Setting):
        self.document = document
        self.setting = setting
        self.executor = setting.executor
        self.bot = setting.bot

    async def data(self) -> SettingData:
        result = await self.document.get()
        d = result.to_dict()
        if d is None:
            return await self.create()

        return SettingData(d)

    async def exists(self) -> bool:
        result = await self.document.get()

        return result.exists

    async def create(self) -> Optional[SettingData]:
        if await self.exists():
            return
        payload = dict(
            name=True,
            emoji=True,
            bot=False,
            limit=100,
            keep=True
        )
        await self.document.set(payload)
        return SettingData(payload)

    async def edit(self,
                   name: Optional[bool] = None,
                   emoji: Optional[bool] = None,
                   bot: Optional[bool] = None,
                   limit: Optional[int] = None,
                   keep: Optional[bool] = None) -> None:
        data = await self.data()
        name = name if name is not None else data.name
        emoji = emoji if emoji is not None else data.emoji
        bot = bot if bot is not None else data.bot
        limit = limit if limit is not None else data.limit
        keep = keep if keep is not None else data.keep

        payload = dict(name=name, emoji=emoji, bot=bot, limit=limit, keep=keep)

        await self.document.set(payload)


class Setting:
    def __init__(self, firestore: 'FireStore') -> None:
        self.bot = firestore.bot
        self.firestore = firestore
        self.db = firestore.db
        self.executor = firestore.executor
        self.collection = self.db.collection('guild_settings')

    def get(self, guild_id: Union[int, str]) -> SettingSnapshot:
        return SettingSnapshot(self.collection.document(str(guild_id)), self)
