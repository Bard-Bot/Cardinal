# mypy: ignore-errors
from __future__ import annotations
from google.cloud.firestore_v1 import AsyncDocumentReference
from typing import Dict, TYPE_CHECKING, Union, Optional, Any

if TYPE_CHECKING:
    from lib import FireStore


class UserSettingData:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    @property
    def voice(self) -> str:
        return self.data['voice']

    @property
    def pitch(self) -> Union[int, float]:
        return self.data['pitch']

    @property
    def speed(self) -> Union[int, float]:
        return self.data['speed']


class UserSettingSnapshot:
    def __init__(self, document: AsyncDocumentReference, user_setting: UserSetting) -> None:
        self.document = document
        self.setting = user_setting
        self.bot = user_setting.bot

    async def data(self) -> Optional[UserSettingData]:
        result = await self.document.get()
        d = result.to_dict()
        if d is None:
            return await self.create()

        return UserSettingData(d)

    async def exists(self) -> bool:
        result = await self.document.get()

        return result.exists

    async def create(self) -> Optional[UserSettingData]:
        if await self.exists():
            return
        payload = dict(
            voice=dict(ja='A', en='A'),  # グローバル設定
            pitch=0.0,
            speed=1.0,
        )

        await self.document.set(payload)
        return UserSettingData(payload)

    async def edit(self,
                   voice: Optional[str] = None,
                   pitch: Optional[Union[int, float]] = None,
                   speed: Optional[Union[int, float]] = None) -> None:
        base = await self.data()
        voice = base.voice if voice is None else voice
        pitch = base.pitch if pitch is None else pitch
        speed = base.speed if speed is None else speed

        payload = dict(voice=voice, pitch=pitch, speed=speed)

        await self.document.set(payload, merge=True)


class UserSetting:
    def __init__(self, firestore: 'FireStore') -> None:
        self.bot = firestore.bot
        self.firestore = firestore
        self.db = firestore.db
        self.collection = self.db.collection('user_setting')

    def get(self, guild_id: Union[int, str]) -> UserSettingSnapshot:
        return UserSettingSnapshot(self.collection.document(str(guild_id)), self)
