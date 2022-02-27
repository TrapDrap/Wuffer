import nextcord,time,asyncio,os,psutil
from datetime import datetime
from nextcord.ext import commands

import config
from data import *

if __name__=='__main__':

#
# Sets the BOT client

    PREFIX=config.PREFIX
    TOKEN=config.TOKEN
    print(f'[{str(datetime.now())[0:-7]}] Prefix: {PREFIX}')
    BOT=commands.Bot(command_prefix=PREFIX,intents=nextcord.Intents.all())

#
## Login event

    @BOT.event
    async def on_ready():
        global pBOTCLIENT,startUpTime
        print(f'[{str(datetime.now())[0:-7]}] Wuffer Bot logged in as {BOT.user}')
        await BOT.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="my About Me"))
        BOT.remove_command('help')
        pBOTCLIENT=BOT.user.id
        startUpTime=str(time.time()).split('.')[0]

#
## Process commands only in guilds

    @BOT.event
    async def on_message(ctx):
        if ctx.author!=BOT.user and ctx.guild is not None:
            await BOT.process_commands(ctx)

#
## Load/Unload/Reload commands

    @BOT.command()
    @commands.has_permissions(administrator=True)
    async def load(ctx,module:str):
        if module.lower()=='all':
            try:
                for file in os.listdir('./modules'):
                    if file.endswith('.py') and not file.startswith('#'):
                        BOT.load_extension(f'modules.{file[:-3]}')
                await ctx.send(embed=nextcord.Embed(description=f'Successfully loaded ALL modules',color=cGREEN))
            except:
                await ctx.send(embed=nextcord.Embed(description=f'Failed to load ALL modules',color=cRED))
        else:
            try:
                BOT.load_extension(f'modules.{module}')
                await ctx.send(embed=nextcord.Embed(description=f'Successfully loaded module `{module}`',color=cGREEN))
            except:
                await ctx.send(embed=nextcord.Embed(description=f'Failed to load module `{module}`',color=cRED))

    @BOT.command()
    @commands.has_permissions(administrator=True)
    async def unload(ctx,module:str):
        if module.lower()=='all':
            try:
                for file in os.listdir('./modules'):
                    if file.endswith('.py') and not file.startswith('#'):
                        BOT.unload_extension(f'modules.{file[:-3]}')
                await ctx.send(embed=nextcord.Embed(description=f'Successfully unloaded ALL modules',color=cGREEN))
            except:
                await ctx.send(embed=nextcord.Embed(description=f'Failed to unload ALL modules',color=cRED))
        else:
            try:
                BOT.unload_extension(f'modules.{module}')
                await ctx.send(embed=nextcord.Embed(description=f'Successfully unloaded module `{module}`',color=cGREEN))
            except:
                await ctx.send(embed=nextcord.Embed(description=f'Failed to unload module `{module}`',color=cRED))

    @BOT.command()
    @commands.has_permissions(administrator=True)
    async def reload(ctx,module:str):
        if module.lower()=='all':
            try:
                for file in os.listdir('./modules'):
                    if file.endswith('.py') and not file.startswith('#'):
                        BOT.unload_extension(f'modules.{file[:-3]}')
                        BOT.load_extension(f'modules.{file[:-3]}')
                await ctx.send(embed=nextcord.Embed(description=f'Successfully reloaded ALL modules',color=cGREEN))
            except:
                await ctx.send(embed=nextcord.Embed(description=f'Failed to reload ALL modules',color=cRED))
        else:
            try:
                BOT.unload_extension(f'modules.{module}')
                BOT.load_extension(f'modules.{module}')
                await ctx.send(embed=nextcord.Embed(description=f'Successfully reloaded module `{module}`',color=cGREEN))
            except:
                await ctx.send(embed=nextcord.Embed(description=f'Failed to reload module `{module}`',color=cRED))

    @BOT.command()
    @commands.has_permissions(administrator=True)
    async def terminate(ctx):
        try:
            for file in os.listdir('./modules'):
                if file.endswith('.py') and not file.startswith('#'):
                    try:
                        BOT.unload_extension(f'modules.{file[:-3]}')
                    except:
                        pass
            await ctx.send(embed=nextcord.Embed(description=f'Terminated every process.',color=cRED))
        except:
            await ctx.send(embed=nextcord.Embed(description=f'Failed to stop... Yikes!'))

    @BOT.command()
    @commands.has_permissions(administrator=True)
    async def startup(ctx):
        try:
            for file in os.listdir('./modules'):
                if file.endswith('.py') and not file.startswith('#'):
                    try:
                        BOT.load_extension(f'modules.{file[:-3]}')
                    except:
                        pass
            await ctx.send(embed=nextcord.Embed(description=f'Reinstated every process.',color=cGREEN))
        except:
            await ctx.send(embed=nextcord.Embed(description=f'Failed to start... Yikes!'))

#
## Statistics commands

    @BOT.command()
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def latency(ctx):
        await ctx.reply(f'My wuff takes {round(BOT.latency*1000)}ms to reach you!',mention_author=False,delete_after=5)
        await asyncio.sleep(5)
        await ctx.message.delete()

    @BOT.command()
    @commands.cooldown(1,10,commands.BucketType.guild)
    async def runtime(ctx):
        permsCheckRoles=ctx.author.roles
        if pADMINROLE in [r.id for r in permsCheckRoles]:
            program=psutil.Process(os.getpid())
            uptime=f'<t:{startUpTime}:R>'
            await ctx.send(f'My current latency is `{round(BOT.latency*1000)} ms`\nCurrent memory usage is `{round(program.memory_info().rss/1048576,2)} mb`\nBot rebooted {uptime}',mention_author=False)
        else:
            await ctx.reply(embed=nextcord.Embed(description='You do not have permission to use this.',color=cGRAY),delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()

#
## Load all modules upon starting code

    for file in os.listdir('./modules'):
        if file.endswith('.py') and not file.startswith('#'):
            BOT.load_extension(f'modules.{file[:-3]}')

#
## Runs the bot 

    BOT.run(TOKEN)