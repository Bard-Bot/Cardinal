from __future__ import annotations
from discord.ext import commands
from typing import Dict, List
from collections import defaultdict
from os import environ
import discord
import asyncio


def _prefix_callable(bot: Cardinal, msg: discord.Message) -> list:
    user_id = bot.user.id
    base = [f'<@!{user_id}> ',
            f'<@{user_id}> ',
            environ.get('PREFIX', '::'),
            'bard::',
            ]

    return base


class Cardinal(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=_prefix_callable,
            help_command=None,
            loop=asyncio.get_event_loop()
        )
        self.joined_bard_bots: Dict[int, List[int]] = defaultdict(list)

    async def on_ready(self) -> None:
        await self.change_presence(
            activity=discord.Game(
                name=f"{environ.get('PREFIX', '::')}help | 読み上げBot"
            )
        )
