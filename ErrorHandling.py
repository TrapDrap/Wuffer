import nextcord
from nextcord.ext import commands
from data import *

class ErrorHandling(commands.Cog):
    def __init__(self,BOT):
        self.BOT=BOT

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.reply(embed=nextcord.Embed(description=str('On cooldown for `{:.2f}s`'.format(error.retry_after)),color=cGRAY),delete_after=5)
            await ctx.message.delete()

def setup(BOT):
    BOT.add_cog(ErrorHandling(BOT))