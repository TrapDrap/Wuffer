import nextcord,asyncio
from nextcord.ext import commands
from data import *
from jsonManager import *
from config import PREFIX

class AffectionCommands(commands.Cog):
    def __init__(self,BOT):
        self.BOT=BOT

#
# AFFECTION COMMANDS BELOW

    @commands.command()
    @commands.cooldown(1,300,commands.BucketType.user)
    async def toggle(self,ctx):
        try: 
            blacklist=loadJson('AffectionBlacklist.json')
            toToggleFromList=str(ctx.author.id)
            
            if toToggleFromList in blacklist:
                blacklist.remove(toToggleFromList)
                saveJson('AffectionBlacklist.json',blacklist)
                await ctx.send(embed=nextcord.Embed(description=str('You have removed your opt-out for affection commands'),color=cGRAY),delete_after=5)
            else:
                blacklist.append(toToggleFromList)
                saveJson('AffectionBlacklist.json',blacklist)
                await ctx.send(embed=nextcord.Embed(description=str('You have been opt out of affection commands'),color=cGRAY),delete_after=5)
        except:
            await ctx.reply(embed=nextcord.Embed(description=f'{vFAIL} **Unknown error**',color=cRED),mention_author=False,delete_after=5)
        await asyncio.sleep(5)
        await ctx.message.delete()

    @commands.command(aliases=['pat','boop','snuggle','snug','cuddle','bap','poke'])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def hug(self,ctx,targetMember:nextcord.Member=None):
        userMention=None
        if targetMember!=None:
            userMention=f'<@{targetMember.id}>'
            ID=str(targetMember.id)
        else:
            embedVar=nextcord.Embed(description='Invalid target',color=cGRAY)
            await ctx.reply(embed=embedVar,delete_after=5)
            await ctx.message.delete()
        
        blacklist=loadJson('AffectionBlacklist.json')

        if userMention is not None:
            if str(ctx.message.content).startswith(f'{PREFIX}hug'):
                if ID not in blacklist:
                    if ID==str(ctx.author.id):
                        embedVar=nextcord.Embed(description=f'<:Hug:924806753735045181> {userMention} hugged themselves... interesting',color=0xfc5176)
                        await ctx.send(embed=embedVar,mention_author=False)
                    elif ID==str(self.BOT.user.id):
                        embedVar=nextcord.Embed(description=f'I was hugged by <@{str(ctx.author.id)}>\nYou seem like you need a hug\n<@{str(self.BOT.user.id)}> has hugged you \\\(>w<)/',color=0xfc5176)
                        await ctx.send(embed=embedVar,mention_author=False)
                    else:
                        embedVar=nextcord.Embed(description=f'<:Hug:924806753735045181> {userMention} was hugged by <@{str(ctx.author.id)}>',color=0xfc5176)
                        await ctx.send(embed=embedVar,mention_author=False)
                else:
                    embedVar=nextcord.Embed(description='<:EmojiSobPuddle:929641372456206376> You cannot hug this person...',color=cGRAY)
                    await ctx.reply(embed=embedVar, delete_after=5)
                    await ctx.message.delete()
                    
            elif str(ctx.message.content).startswith(f'{PREFIX}pat'):
                if ID not in blacklist:
                    if ID==str(ctx.author.id):
                        embedVar = nextcord.Embed(description=f'<a:Pat:920690234503602207> {userMention} pat themselves... how?',color=0xfc8353)
                        await ctx.send(embed=embedVar,mention_author=False)
                    elif ID==str(self.BOT.user.id):
                        embedVar = nextcord.Embed(description=f'<a:Pat:920690234503602207> I was pat by <@{str(ctx.author.id)}> (˶ •. • ˶)',color=0xfc8353)
                        await ctx.send(embed=embedVar,mention_author=False)
                    else:
                        embedVar = nextcord.Embed(description=f'<a:Pat:920690234503602207> {userMention} was pat by <@{str(ctx.author.id)}>',color=0xfc8353)
                        await ctx.send(embed=embedVar,mention_author=False)
                else:
                    embedVar=nextcord.Embed(description='<:EmojiSobPuddle:929641372456206376> You cannot pat this person...',color=cGRAY)
                    await ctx.reply(embed=embedVar, delete_after=5)
                    await ctx.message.delete()

            elif str(ctx.message.content).startswith(f'{PREFIX}boop'):
                if ID not in blacklist:
                    if ID==str(ctx.author.id):
                        embedVar=nextcord.Embed(description=f'<a:Boop:924806780205273108> {userMention} booped themselves... impressive!',color=0xf58cff)
                        await ctx.send(embed=embedVar,mention_author=False)
                    elif ID==str(self.BOT.user.id):
                        embedVar=nextcord.Embed(description=f'<a:Boop:924806780205273108> <@{str(ctx.author.id)}> gently booped my snoot (>///<)',color=0xf58cff)
                        await ctx.send(embed=embedVar,mention_author=False)
                    else:
                        embedVar=nextcord.Embed(description=f'<a:Boop:924806780205273108> <@{str(ctx.author.id)}> gently booped {userMention}',color=0xf58cff)
                        await ctx.send(embed=embedVar,mention_author=False)
                else:
                    embedVar=nextcord.Embed(description='<:EmojiSobPuddle:929641372456206376> You cannot boop this person...',color=cGRAY)
                    await ctx.reply(embed=embedVar, delete_after=5)
                    await ctx.message.delete()
                    
            elif str(ctx.message.content).startswith(f'{PREFIX}cuddle'):
                if ID not in blacklist:
                    if ID==str(ctx.author.id):
                        embedVar=nextcord.Embed(description=f'<:Cuddle:924806978075762739> {userMention} cuddled themselves... mmm...',color=0xfc5181)
                        await ctx.send(embed=embedVar,mention_author=False)
                    elif ID==str(self.BOT.user.id):
                        embedVar=nextcord.Embed(description=f'<:Cuddle:924806978075762739> <@{str(ctx.author.id)}> cuddled with me (〃>///<〃)',color=0xfc5181)
                        await ctx.send(embed=embedVar,mention_author=False)
                    else:
                        embedVar=nextcord.Embed(description=f'<:Cuddle:924806978075762739> <@{str(ctx.author.id)}> cuddled {userMention}',color=0xfc5181)
                        await ctx.send(embed=embedVar,mention_author=False)
                else:
                    embedVar=nextcord.Embed(description='<:EmojiSobPuddle:929641372456206376> You cannot cuddle this person...',color=cGRAY)
                    await ctx.reply(embed=embedVar, delete_after=5)
                    await ctx.message.delete()
            
            elif str(ctx.message.content).startswith(f'{PREFIX}snug'):
                if ID not in blacklist:
                    if ID==str(ctx.author.id):
                        embedVar=nextcord.Embed(description=f'<a:Snuggle:924806957498507314> {userMention} snuggled themselves... hmmm...',color=0xff8cb8)
                        await ctx.send(embed=embedVar,mention_author=False)
                    elif ID==str(self.BOT.user.id):
                        embedVar=nextcord.Embed(description=f'<a:Snuggle:924806957498507314> <@{str(ctx.author.id)}> snuggled me (ˊ•///•ˋ)',color=0xff8cb8)
                        await ctx.send(embed=embedVar,mention_author=False)
                    else:
                        embedVar=nextcord.Embed(description=f'<a:Snuggle:924806957498507314> <@{str(ctx.author.id)}> snuggled {userMention}',color=0xff8cb8)
                        await ctx.send(embed=embedVar,mention_author=False)
                else:
                    embedVar=nextcord.Embed(description='<:EmojiSobPuddle:929641372456206376> You cannot snuggle this person...',color=cGRAY)
                    await ctx.reply(embed=embedVar, delete_after=5)
                    await ctx.message.delete()
            
            elif str(ctx.message.content).startswith(f'{PREFIX}poke'):
                if ID not in blacklist:
                    if ID==str(ctx.author.id):
                        embedVar=nextcord.Embed(description=f'<a:Poke:928135870714884157> {userMention} poked themselves... it seems you like to suffer',color=0xffefeb)
                        await ctx.send(embed=embedVar,mention_author=False)
                    elif ID==str(self.BOT.user.id):
                        embedVar=nextcord.Embed(description=f'<a:Poke:928135870714884157> <@{str(ctx.author.id)}> poked me (｡•́ - •̀｡)',color=0xffefeb)
                        await ctx.send(embed=embedVar,mention_author=False)
                    else:
                        embedVar=nextcord.Embed(description=f'<a:Poke:928135870714884157> {userMention} was poked by <@{str(ctx.author.id)}>',color=0xffefeb)
                        await ctx.send(embed=embedVar,mention_author=False)
                else:
                    embedVar=nextcord.Embed(description='<:EmojiSobPuddle:929641372456206376> You cannot poke this person...',color=cGRAY)
                    await ctx.reply(embed=embedVar, delete_after=5)
                    await ctx.message.delete()

            elif str(ctx.message.content).startswith(f'{PREFIX}bap'):
                if ID not in blacklist:
                    if ID==str(ctx.author.id):
                        embedVar=nextcord.Embed(description=f'<a:Bap:928137010554740756> {userMention} bapped themselves... why would one do such a thing?',color=0x3bcaeb)
                        await ctx.send(embed=embedVar,mention_author=False)
                    elif ID==str(self.BOT.user.id):
                        embedVar=nextcord.Embed(description=f'<a:Bap:928137010554740756> I got bapped by <@{str(ctx.author.id)}> (｡Ó﹏Ò｡)',color=0x3bcaeb)
                        await ctx.send(embed=embedVar,mention_author=False)
                    else:
                        embedVar=nextcord.Embed(description=f'<a:Bap:928137010554740756> {userMention} got bapped by <@{str(ctx.author.id)}>',color=0x3bcaeb)
                        await ctx.send(embed=embedVar,mention_author=False)
                else:
                    embedVar=nextcord.Embed(description='<:EmojiSobPuddle:929641372456206376> You cannot bap this person...',color=cGRAY)
                    await ctx.reply(embed=embedVar, delete_after=5)
                    await ctx.message.delete()
        else:
            embedVar=nextcord.Embed(description='Invalid target',color=cGRAY)
            await ctx.reply(embed=embedVar,delete_after=5)
            await ctx.message.delete()

def setup(BOT):
    BOT.add_cog(AffectionCommands(BOT))