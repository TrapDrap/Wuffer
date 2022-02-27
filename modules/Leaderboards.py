import nextcord,asyncio
from nextcord.ext import commands
from datetime import datetime
from data import *
from jsonManager import *

#
# LEADERBOARD STUFF

disboardTimer=None
reminderLoop=None

def getMemberBumpCount(toFind):
    leaderboardList=loadJson('Leaderboard.json')
    try:
        position=leaderboardList.index(toFind)
    except:
        position=None
    if position!=None:
        return leaderboardList[position+1]
    else:
        return 0

def getLeaderboard():
    leaderboardList=loadJson('Leaderboard.json')
    fileLength=len(leaderboardList)
    toSort=[]
    for i in range(1,fileLength,2):
        toSort.append(leaderboardList[i])
    finalLeaderboard=[]
    if fileLength>40:
        for i in range(20):
            pos=toSort.index(max(toSort))
            toSort[pos]=0
            pos=(pos*2)+1
            finalLeaderboard.append(leaderboardList[pos-1])
            finalLeaderboard.append(leaderboardList[pos])
    else:
        for i in range(len(toSort)):
            pos=toSort.index(max(toSort))
            toSort[pos]=0
            pos=(pos*2)+1
            finalLeaderboard.append(leaderboardList[pos-1])
            finalLeaderboard.append(leaderboardList[pos])
    return finalLeaderboard

async def bumpCountdown(self,minutesLeft):
    global disboardTimer,timeLeft
    bumpChannel=self.BOT.get_channel(pBUMPCHANNEL)
    timeLeft=int(minutesLeft)
    if timeLeft>0:
        while timeLeft!=0:
            await asyncio.sleep(60)
            timeLeft-=1
    await bumpChannel.send(f'<@&{pBUMPERROLE}>',embed=nextcord.Embed(description=f"<:EmojiHearts:930884280924639272> Looks like it's time to bump! Use `!d bump`",color=cVIOLET))

async def startTimer(Self):
    global disboardTimer
    disboardTimer=asyncio.create_task(bumpCountdown(Self,120))
    print(f'[{str(datetime.now())[0:-7]}] Starting timer has been initiated')
    
class Leaderboards(commands.Cog):
    def __init__(self,BOT):
        global disboardTimer
        self.BOT=BOT
        print(self.BOT)
        try:
            if disboardTimer is None:
                asyncio.create_task(startTimer(self))
        except:
            pass

    @commands.Cog.listener()
    async def on_ready(self):
        global disboardTimer
        if disboardTimer is None:
            asyncio.create_task(startTimer(self))

    # Leaderboard Command
    @commands.command(aliases=['topbumpers','bumplb','bumps'])
    @commands.cooldown(1,5,commands.BucketType.guild)
    async def bumpleaderboard(self,ctx):
        if ctx.channel.id==pBUMPCHANNEL or ctx.channel.id==pTESTCHANNEL or ctx.channel.id==pBOTSCHANNEL:
            leaderboard=getLeaderboard()
            textFormLeaderboard=str()
            leaderboardLength=int(len(leaderboard)/2)
            for i in range(leaderboardLength):
                textFormLeaderboard+=f'**{i+1}.** <@{leaderboard[i*2]}>: '
                if leaderboard[i*2+1]==1:
                    textFormLeaderboard+=f'{leaderboard[i*2+1]} Bump\n'
                else:
                    textFormLeaderboard+=f'{leaderboard[i*2+1]} Bumps\n'
            leaderboardEmbed=nextcord.Embed(title='Leaderboard of Top Bumpers',description=f'{textFormLeaderboard}',color=cVIOLET)
            leaderboardEmbed.set_footer(text=f'Your bump count: {getMemberBumpCount(str(ctx.author.id))}',icon_url=ctx.author.display_avatar)
            await ctx.send(embed=leaderboardEmbed)

    #BUMP DETECTION
    @commands.Cog.listener()
    async def on_message(self,ctx):
        global disboardTimer,timeLeft
        if ctx.channel.id==pBUMPCHANNEL:
            if ctx.author.id==pDISBOARDBOT:
                embedFromMessage=ctx.embeds[0]
                bumpInformation=embedFromMessage.description

                if 'Please wait another' in bumpInformation:
                    await ctx.delete()
                    
                    detectionStart=bumpInformation.find('another ')
                    detectionEnd=bumpInformation.find('minute')
                    timeUntilBump=bumpInformation[detectionStart+8:detectionEnd-1]
                    try:
                        timeUntilBump=int(timeUntilBump)
                    except:
                        await ctx.channel.send('Error gathering bump time from Disboard')
                    
                    if (timeLeft-timeUntilBump)>3:
                        if disboardTimer is not None:
                            disboardTimer.cancel()
                        disboardTimer=asyncio.create_task(bumpCountdown(self,timeUntilBump))
                        print(f'[{str(datetime.now())[0:-7]}] Timer task replaced')
                        if timeUntilBump==1:
                            await ctx.channel.send(embed=nextcord.Embed(description=f'Bump timer task has been replaced! ({timeUntilBump} minute)',color=cVIOLET))
                        else:
                            await ctx.channel.send(embed=nextcord.Embed(description=f'Bump timer task has been replaced! ({timeUntilBump} minutes)',color=cVIOLET))
                    if timeUntilBump==1:
                        await ctx.channel.send(embed=nextcord.Embed(description=f'<:EmojiInnocent:930884239665274950> It appears you have to wait {timeUntilBump} more minute! Get the bumper role [**here**](https://discord.com/channels/779094028327059540/835058468582064129/931175673844871188)',color=cVIOLET))
                    elif timeUntilBump==120:
                        await ctx.channel.send(embed=nextcord.Embed(description=f'<:EmojiShy:930890239889772565> It seems like you were too slow... Good luck next time!',color=cLIGHTAQUA))
                    else:
                        await ctx.channel.send(embed=nextcord.Embed(description=f'<:EmojiInnocent:930884239665274950> It appears you have to wait {timeUntilBump} more minutes! Get the bumper role [**here**](https://discord.com/channels/779094028327059540/835058468582064129/931175673844871188)',color=cVIOLET))
                
                elif 'Bump done!' in bumpInformation:
                    if disboardTimer is not None:
                        disboardTimer.cancel()
                    disboardTimer=asyncio.create_task(bumpCountdown(self,120))
                    
                    bumper=str(bumpInformation.split()[0]).replace('<','').replace('@','').replace('!','').replace('>','').replace(' ','')
                    leaderboardData=loadJson('Leaderboard.json')
                    if bumper not in leaderboardData:
                        leaderboardData.append(bumper)
                        leaderboardData.append(1)
                    else:
                        position=leaderboardData.index(bumper)
                        value=leaderboardData[position+1]
                        leaderboardData[position+1]=value+1
                    saveJson('Leaderboard.json',leaderboardData)
                    successEmbed=nextcord.Embed(description='<:EmojiLoved:932104744107900928> Awesome! Your bump has registered!',color=cVIOLET)
                    userBumps=getMemberBumpCount(bumper)
                    if userBumps==1:
                        successEmbed.set_footer(text=f'You now have {userBumps} total bump')
                    else:
                        successEmbed.set_footer(text=f'You now have {userBumps} total bumps')
                    await ctx.channel.send(f'<@{bumper}>',embed=successEmbed)

                elif 'handling your command!' in bumpInformation:
                    await ctx.delete()
                    await ctx.channel.send(embed=nextcord.Embed(description='<:EmojiWTF:921099443216986144> Too many people bumping at once...',color=cRED))
                    
                else:
                    await ctx.delete()
                    
                    await ctx.channel.send(embed=nextcord.Embed(description='<:EmojiWTF:921099443216986144> It seems you entered the wrong command. Use `!d bump`',color=cVIOLET))

def setup(BOT):
    BOT.add_cog(Leaderboards(BOT))
