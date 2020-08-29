# mypy: ignore-errors
from .embed import Success, Error, Notice, Admin, Default  # noqa
from .firestore import FireStore  # noqa
from .firestore.guild_dict import GuildDict
from .firestore.guild import GuildData
from .firestore.guild_setting import SettingData
from .firestore.user_setting import UserSettingData


BARD_BOTS = [
    727687910643466271,
    739831545283477525,
]
