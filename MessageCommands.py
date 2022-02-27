import nextcord,asyncio,json
from nextcord.ext import commands
from data import *

class MessageCommands(commands.Cog):
    def __init__(self,BOT):
        self.BOT=BOT

    @commands.command(aliases=['say','send'])
    async def echo(self,ctx,targetChannel:nextcord.TextChannel,*,messageToEcho):
        permsCheckRoles=ctx.author.roles
        rolesToCheck=[r.id for r in permsCheckRoles]
        if pADMINROLE in rolesToCheck:
            messageToEcho=str(messageToEcho).replace('{{','<').replace('}}','>')
            await targetChannel.send(messageToEcho,allowed_mentions=nextcord.AllowedMentions())
            await ctx.message.add_reaction(vCONFIRM)
        elif pSTAFFROLE in rolesToCheck:
            messageToEcho=str(messageToEcho).replace('{{','<').replace('}}','>')
            await targetChannel.send(messageToEcho,allowed_mentions=nextcord.AllowedMentions(everyone=False,roles=False))
            await ctx.message.add_reaction(vCONFIRM)
        else:
            await ctx.reply(embed=nextcord.Embed(description='You do not have permission to use this.',color=cGRAY),delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()

    @commands.command(aliases=['edit'])
    async def editmsg(self,ctx,targetChannel:nextcord.TextChannel,targetMessageID,*,newMessage):
        permsCheckRoles=ctx.author.roles
        if pADMINROLE in [r.id for r in permsCheckRoles]:
            targetMessage=targetChannel.get_partial_message(int(targetMessageID))
            newMessage=str(newMessage).replace('{{','<').replace('}}','>')
            await targetMessage.edit(content=newMessage)
            await ctx.message.add_reaction(vCONFIRM)
        else:
            await ctx.reply(embed=nextcord.Embed(description='You do not have permission to use this.',color=cGRAY),delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()

    @commands.command(aliases=['message','msg'])
    async def dm(self,ctx,toDM:nextcord.Member=None,*,msg=None):
        if toDM is not None:
            permsCheckRoles=ctx.author.roles
            verifiedCheckRoles=toDM.roles
            permsCheckRoleIDs=[r.id for r in permsCheckRoles]
            if pSTAFFROLE in permsCheckRoleIDs or pINVISSTAFFROLE in permsCheckRoleIDs:
                if pVERIFIEDROLE in [r.id for r in verifiedCheckRoles]:
                    try:
                        toDMTag=str(toDM)
                        if msg!=None:
                            dmEmbedVar=nextcord.Embed(description=f'You have received a message from the Staff Team:\n\n{msg}',color=cLIGHTAQUA)
                            dmEmbedVar.set_author(name=ctx.guild.name,icon_url=ctx.guild.icon)
                            try:
                                await toDM.send(embed=dmEmbedVar)
                                await ctx.reply(embed=nextcord.Embed(description=f'{vCONFIRM} {toDMTag} **has received the message**',color=cLIGHTRED),mention_author=False)
                            except:
                                await ctx.reply(embed=nextcord.Embed(description='**Target unable to receive DMs**',color=cDARKCYAN),mention_author=False)
                        else:
                            await ctx.reply(embed=nextcord.Embed(description=f'{vFAIL} **Message not provided**',color=cRED),mention_author=False)
                    except:
                        await ctx.reply(embed=nextcord.Embed(description=f'{vFAIL} **Unknown error**',color=cRED),mention_author=False)
                else:
                    await ctx.reply(embed=nextcord.Embed(description=f'{vFAIL} You cannot DM an unverified member! Use `.ask`',color=cRED),mention_author=False)
            else:
                await ctx.reply(embed=nextcord.Embed(description='You do not have permission to use this.',color=cGRAY),delete_after=5)
                await asyncio.sleep(5)
                await ctx.message.delete()
        else:
            embedVar=nextcord.Embed(description='Invalid target',color=cGRAY)
            await ctx.reply(embed=embedVar,delete_after=5)
            await ctx.message.delete()

    @commands.command(aliases=['messagestaff','msgstaff'])
    async def dmstaff(self,ctx,toDM:nextcord.Member=None,*,msg=None):
        if toDM is not None:
            permsCheckRoles=ctx.author.roles
            staffCheckRoles=toDM.roles
            permsCheckRoleIDs=[r.id for r in permsCheckRoles]
            if pADMINROLE in permsCheckRoleIDs or pMODPLUSROLE in permsCheckRoleIDs:
                if pSTAFFROLE in [r.id for r in staffCheckRoles]:
                    try:
                        toDMTag=str(toDM)
                        if msg!=None:
                            dmEmbedVar=nextcord.Embed(description=f'Message from the Management Team:\n\n{msg}',color=cLIGHTAQUA)
                            dmEmbedVar.set_author(name=ctx.guild.name,icon_url=ctx.guild.icon)
                            try:
                                await toDM.send(embed=dmEmbedVar)
                                await ctx.reply(embed=nextcord.Embed(description=f'{vCONFIRM} {toDMTag} **has received the staff message**',color=cLIGHTRED),mention_author=False)
                            except:
                                await ctx.reply(embed=nextcord.Embed(description='**Target unable to receive DMs**',color=cDARKCYAN),mention_author=False)
                        else:
                            await ctx.reply(embed=nextcord.Embed(description=f'{vFAIL} **Message not provided**',color=cRED),mention_author=False)
                    except:
                        await ctx.reply(embed=nextcord.Embed(description=f'{vFAIL} **Unknown error**',color=cRED),mention_author=False)
                else:
                    await ctx.reply(embed=nextcord.Embed(description=f'{vFAIL} You cannot DMstaff a non-staff member! Use `.dm`',color=cRED),mention_author=False)
            else:
                await ctx.reply(embed=nextcord.Embed(description='You do not have permission to use this.',color=cGRAY),delete_after=5)
                await asyncio.sleep(5)
                await ctx.message.delete()
        else:
            embedVar=nextcord.Embed(description='Invalid target',color=cGRAY)
            await ctx.reply(embed=embedVar,delete_after=5)
            await ctx.message.delete()

    @commands.command()
    async def dmraw(self,ctx,toDM:nextcord.Member=None,*,msg=None):
        if toDM is not None:
            permsCheckRoles=ctx.author.roles
            permsCheckRoleIDs=[r.id for r in permsCheckRoles]
            if pADMINROLE in permsCheckRoleIDs:
                try:
                    toDMTag=str(toDM)
                    if msg!=None:
                        try:
                            await toDM.send(msg)
                            await ctx.reply(embed=nextcord.Embed(description=f'{vCONFIRM} {toDMTag} **has received the raw message**',color=cLIGHTRED),mention_author=False)
                        except:
                            await ctx.reply(embed=nextcord.Embed(description='**Target unable to receive DMs**',color=cDARKCYAN),mention_author=False)
                    else:
                        await ctx.reply(embed=nextcord.Embed(description=f'{vFAIL} **Message not provided**',color=cRED),mention_author=False)
                except:
                    await ctx.reply(embed=nextcord.Embed(description=f'{vFAIL} **Unknown error**',color=cRED),mention_author=False)
            else:
                await ctx.reply(embed=nextcord.Embed(description='You do not have permission to use this.',color=cGRAY),delete_after=5)
                await asyncio.sleep(5)
                await ctx.message.delete()
        else:
            embedVar=nextcord.Embed(description='Invalid target',color=cGRAY)
            await ctx.reply(embed=embedVar,delete_after=5)
            await ctx.message.delete()

    @commands.command()
    async def dmembed(self,ctx,targetChannel:nextcord.Member,*,unformattedJsonData=None):
        permsCheckRoles=ctx.author.roles
        if pADMINROLE in [r.id for r in permsCheckRoles]:
            try:
                jsonData=json.loads(unformattedJsonData)
                
                try:
                    if jsonData is not None:
                        
                        plainText=None
                        titleText=nextcord.Embed.Empty
                        titleUrl=nextcord.Embed.Empty
                        description=nextcord.Embed.Empty
                        authorName=nextcord.Embed.Empty
                        authorUrl=nextcord.Embed.Empty
                        authorIconUrl=nextcord.Embed.Empty
                        color=nextcord.Embed.Empty
                        thumbnailUrl=nextcord.Embed.Empty
                        imageUrl=nextcord.Embed.Empty
                        fieldLength=None
                        fields=None
                        footerText=nextcord.Embed.Empty
                        footerIconUrl=nextcord.Embed.Empty

                        # All of the embed datatypes
                        if 'plainText' in jsonData:
                            plainText=jsonData['plainText']
                        if 'title' in jsonData:
                            titleText=jsonData['title']
                        if 'url' in jsonData:
                            titleUrl=jsonData['url']
                        if 'description' in jsonData:
                            description=jsonData['description']
                        if 'author' in jsonData:
                            for e in jsonData['author']:
                                if 'name' in jsonData['author']:
                                    authorName=jsonData['author']['name']
                                if 'url' in jsonData['author']:
                                    authorUrl=jsonData['author']['url']
                                if 'icon_url' in jsonData['author']:
                                    authorIconUrl=jsonData['author']['icon_url']
                        if 'color' in jsonData:
                            color=jsonData['color']
                        if 'thumbnail' in jsonData:
                            thumbnailUrl=jsonData['thumbnail']
                        if 'image' in jsonData:
                            imageUrl=jsonData['image']
                        if 'fields' in jsonData:
                            fieldLength=len(jsonData['fields'])
                            fields=[]
                            for fieldNum in jsonData['fields']:
                                if 'name' in fieldNum:
                                    fields.append(fieldNum['name'])
                                else:
                                    fields.append(None)
                                if 'value' in fieldNum:
                                    fields.append(fieldNum['value'])
                                else:
                                    fields.append(None)
                                if 'inline' in fieldNum:
                                    fields.append(fieldNum['inline'])
                                else:
                                    fields.append(None)
                        if 'footer' in jsonData:
                            for j in jsonData['footer']:
                                if 'text' in jsonData['footer']:
                                    footerText=jsonData['footer']['text']
                                if 'icon_url' in jsonData['footer']:
                                    footerIconUrl=jsonData['footer']['icon_url']
                        #

                        # Build the embed
                        jsonEmbed=nextcord.Embed(title=titleText, url=titleUrl, description=description, color=color)
                        if authorName!=nextcord.Embed.Empty:
                            jsonEmbed.set_author(name=authorName, url=authorUrl, icon_url=authorIconUrl)
                        jsonEmbed.set_thumbnail(url=thumbnailUrl)
                        jsonEmbed.set_image(url=imageUrl)
                        if fieldLength!=None:
                            for i in range(fieldLength):
                                if fields[2+3*i] is None:
                                    jsonEmbed.add_field(name=fields[0+3*i], value=fields[1+3*i])
                                elif fields[2+3*i] is not None:
                                    jsonEmbed.add_field(name=fields[0+3*i], value=fields[1+3*i], inline=fields[2+3*i])
                        jsonEmbed.set_footer(text=footerText,icon_url=footerIconUrl)
                        #
                        
                        # Send the embed
                        if plainText!=None:
                            await targetChannel.send(plainText,embed=jsonEmbed)
                        else:
                            sentEmbed=await targetChannel.send(embed=jsonEmbed)
                        await ctx.send(embed=nextcord.Embed(description=f'{vCONFIRM} [**Embed**](https://discord.com/channels/{sentEmbed.author.guild.id}/{targetChannel.id}/{sentEmbed.id}) was successfully sent to DMs',color=cGREEN))
                        #
                    else:
                        await ctx.send(embed=nextcord.Embed(description='**No JSON provided**',color=cDARKCYAN))
                except:
                    await ctx.send(embed=nextcord.Embed(description=f'{vFAIL} **Something broke!**',color=cRED))
            except:
                await ctx.send(embed=nextcord.Embed(description='**JSON Invalid | Build the Embed JSON at https://embedbuilder.nadekobot.me/**',color=cDARKCYAN))
                jsonData=None
        else:
            await ctx.reply(embed=nextcord.Embed(description='You do not have permission to use this.',color=cGRAY),delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()

def setup(BOT):
    BOT.add_cog(MessageCommands(BOT))