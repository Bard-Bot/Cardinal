from discord.ext import commands
from dataclasses import dataclass
from typing import TYPE_CHECKING
import discord


if TYPE_CHECKING:
    from bot import Cardinal


BARD_BOTS = [
    727687910643466271,
    739831545283477525,
]


@dataclass
class BardCheck(commands.Cog):
    bot: 'Cardinal'

    @commands.Cog.listener(name='on_voice_state_update')
    async def check_bard(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        if member.id not in BARD_BOTS:
            return
        if before.channel is None and after.channel is not None:
            # 入った時
            self.bot.joined_bard_bots.append(member.id)
        if member.id in self.bot.joined_bard_bots:
            if before.channel is not None and after.channel is None:
                self.bot.joined_bard_bots.remove(member.id)


def setup(bot: 'Cardinal') -> None:
    return bot.add_cog(BardCheck(bot))
