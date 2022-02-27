import time,asyncio
from nextcord.ext import commands
from datetime import datetime
from data import *

async def getLatestMessage(channelToFindMessageIn,userID):
    global msgToSort
    fetchedMessage=await channelToFindMessageIn.history(limit=10).find(lambda m: m.author.id==userID)
    if fetchedMessage is not None:
        msgToSort.append(fetchedMessage)

class AmariToReaction(commands.Cog):
    def __init__(self,BOT):
        self.BOT=BOT
    
    @commands.Cog.listener()
    async def on_message(self,ctx):
        global msgToSort
    #LEVELUP DETECTION
        if ctx.channel.id==pLEVELUPCHANNEL:
            if ctx.author.id==pAMARI or ctx.author.id==484541026636136449:
                
                triggerTime=time.time()
                
                startTime=time.time()
                msgToSort=[]
                
                msgContent=str(ctx.content).replace('<','').replace('>','').replace('!','').replace('@','')
                user_id=int(msgContent)
                
                channels=ctx.guild.text_channels
                gatheringTasks=[]
                for channel in channels:
                    gatheringTasks.append(asyncio.create_task(getLatestMessage(channel,user_id)))
                
                for task in gatheringTasks:
                    while task.done()!=True:
                        await asyncio.sleep(0.005)
                #print(f'[{str(datetime.now())[0:-7]}] Gathered messages in {time.time()-startTime} seconds')
            
                if msgToSort!=[]:
                    oldestMessage=msgToSort[0]
                    if len(msgToSort)==1:
                        pass
                    else:
                        #print(f'[{str(datetime.now())[0:-7]}] To Sort Count: {len(msgToSort)}')
                        for msg in msgToSort:
                            if msg.created_at>oldestMessage.created_at:
                                oldestMessage=msg
                                #print(f'[{str(datetime.now())[0:-7]}] Replaced Oldest Message')

                    if triggerTime-datetime.timestamp(oldestMessage.created_at) < 12:
                        try:
                            await oldestMessage.add_reaction(vCHEERS)
                        except:
                            pass
                    else:
                        print(f'[{str(datetime.now())[0:-7]}] Message too old by {triggerTime-datetime.timestamp(oldestMessage.created_at)} seconds | msg: {oldestMessage.jump_url} trigger:{ctx.jump_url}')
                    msgToSort=None

                    print(f'[{str(datetime.now())[0:-7]}] Finished everything in {time.time()-startTime} seconds')
                    startTime=None

def setup(BOT):
    BOT.add_cog(AmariToReaction(BOT))
