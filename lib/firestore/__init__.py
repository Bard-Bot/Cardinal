from .guild import Guild
from .guild_setting import Setting
from .guild_dict import GuildDict
from .user_setting import UserSetting
from google.cloud.firestore import AsyncClient
import google.auth
import concurrent.futures
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from bot import Cardinal


class FireStore:
    def __init__(self, bot: 'Cardinal') -> None:
        """
        プランと残り文字数、プランへお金を出した人を保存する
        :param bot: discord.ext.commands.Bot
        """
        credentials, project = google.auth.default(
            scopes=['https://www.googleapis.com/auth/cloud-platform'])

        # TODO: credentialsをasyncio対応にする
        self.bot = bot
        self.db = AsyncClient(credentials=credentials)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
        self.guild = Guild(self)
        self.setting = Setting(self)
        self.dict = GuildDict(self)
        self.user = UserSetting(self)
