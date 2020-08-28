from discord.ext import commands
from dataclasses import dataclass
from typing import TYPE_CHECKING
from lib import BARD_BOTS
import discord


if TYPE_CHECKING:
    from bot import Cardinal


@dataclass
class Voice(commands.Cog):
    bot: 'Cardinal'

    def is_next_join(self) -> bool:
        """このCardinalが次に入るBardかどうかを判定"""
        bots = BARD_BOTS[:]
        for bot in self.bot.joined_bard_bots:
            bots.remove(bot)
        if not bots:
            return False

        return self.bot.user.id == bots[0]

    @commands.command()
    async def join(self, ctx: commands.Context) -> None:
        if not self.is_next_join():
            return

        async with ctx.channel.typing():
            pass


def setup(bot: 'Cardinal') -> None:
    return bot.add_cog(Voice(bot))
