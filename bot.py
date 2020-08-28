from discord.ext import commands
from os import environ
import discord
import asyncio


def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ',
            f'<@{user_id}> ',
            environ.get('prefix', '::'),
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

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Game(
                name=f"{environ.get('prefix', '::')}help | 読み上げBot"
            )
        )
