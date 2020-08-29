from discord import Embed
from discord.ext import commands
from typing import Dict, Any, Optional


class TimestampEmbed(Embed):
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
        ctx: Optional[commands.Context] = kwargs.pop('ctx', None)
        if ctx is not None:
            self.timestamp = ctx.message.created_at


class Error(TimestampEmbed):
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self.color = 0xFF5252


class Success(TimestampEmbed):
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self.color = 0x4CAF50


class Default(TimestampEmbed):
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self.color = 0x197fd2


class Admin(TimestampEmbed):
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self.color = 0xFFC107


class Notice(TimestampEmbed):
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self.color = 0xFFC107
