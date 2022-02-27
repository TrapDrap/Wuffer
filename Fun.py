import nextcord,random
from nextcord.ext import commands
from data import *

class Fun(commands.Cog):
    def __init__(self,BOT):
        self.BOT=BOT

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def choosemember(self,ctx,members:commands.Greedy[nextcord.Member]):
        memberCount=len(members)
        randomMember=members[random.randint(0,memberCount)]
        await ctx.send(embed=nextcord.Embed(description=f'{randomMember.mention}',color=cLIGHTAQUA).set_author(icon_url=randomMember.display_avatar.url,name='I choose...'))

def setup(BOT):
    BOT.add_cog(Fun(BOT))