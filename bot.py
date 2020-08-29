from __future__ import annotations
from discord.ext import commands
from typing import Dict, List, Optional
from collections import defaultdict
from lib import TokenGenerator, FireStore
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
        self.token_generator = TokenGenerator(environ["GOOGLE_APPLICATION_CREDENTIALS"])
        self.google_cloud_token: Optional[str] = None
        self.firestore = FireStore(self)

    async def on_ready(self) -> None:
        await self.change_presence(
            activity=discord.Game(
                name=f"{environ.get('PREFIX', '::')}help | 読み上げBot"
            )
        )

    async def google_cloud_token_loop(self) -> None:
        while not self.is_closed():
            self.google_cloud_token = await self.token_generator.get()
            await asyncio.sleep(3000)
