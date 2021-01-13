# Work with Python 3.6
import discord
from discord.utils import find
import db
import settings as cfg
import wow
import httpserver

TOKEN = cfg.token

client = discord.Client()

httpserver.client = client

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # we do not want the bot to reply to other bots
    if message.author.bot is True:
        return
    
    print(message.author.name + ": " + message.content)

    if message.content.startswith('!mplus hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
        
    if message.content.startswith('!mplus register'):
        """not finished"""
        #get user id
        #generate URL and use it as part of the unique state id
        if message.channel.type == discord.ChannelType.private:
            await message.author.send("Mythic Plus Bot cannot respond to some commands in private channels. Try the `register` command in a Discord Server where this bot has an online presence.")
        else:
            gID = message.guild.id
            registermessage = " \
Thank you for choosing Mythic Plus Bot! Click this link to get going! \n\n\
\
" + cfg.botBaseUrl + "?url=https%3A%2F%2Fus.battle.net%2Foauth%2Fauthorize%3Fscope%3Dwow.profile%26client_id%3D" \
            + cfg.wowClientId + "%26state%3DUID" + str(message.author.id) \
            + "%26redirect_uri%3Dhttps%3A%2F%2F90040ceab0094ad6a2e4a6c8c3376d89.vfs.cloud9.us-east-2.amazonaws.com%3A8080%2Foauth%2Fcallback%26response_type%3Dcode"
            try:
                await message.author.send(registermessage)
                await message.channel.send(str(message.author.mention) + ", I attempted to send you a direct message with instructions on what to do to register a character.")
            except discord.errors.Forbidden:
                await message.channel.send("{0.author.mention}, I can't send you a direct message! \n\n \
 \
Please allow members of this Discord Server to send you a direct message to continue. \n\n \
 \
Please see online help for instructions on how to do this. It is important that the Mythic Plus Bot be able to send you private messages.".format(message))
        
    if message.content.startswith('!mplus add'):
        emdesc = ""
        emtitle = ""
        if message.channel.type == discord.ChannelType.private:
            await message.author.send("Mythic Plus Bot cannot respond to some commands in private channels. Try the `add` command in a Discord Server where this bot has an online presence.")
        else:
            #remove prefix and only select the character name.
            characterName = message.content[10:].strip()
            cname = None
            region = None
            if characterName.find(' ') > -1:
                cname = characterName.split(' ')[0]
                region = characterName.split(' ')[1]
            else:
                cname = characterName
            #search for character only within user's account
            #   if multiple characters are found with the same name, ask user to specify which character
            characters = db.findCharacterByName(cname, region)
            msg = None
            if len(characters) > 1:
                msg = (message.author.mention + ', multiple characters were found with the name `' + characterName + '`. Please specify realm by using the format `character realm`').format(message)
                # get author UID
                uid = message.author.id
                # look in users for bid
                bid = db.getBIDfromDiscordUser(uid)
                # get list of characters belonging to bid
                characterList = db.listAllCharactersWithName(bid, cname)
                for cha in characterList:
                    #print(cha)
                    emdesc += cha[2] + ' - ' + cha[4] + ' - Level: ' + str(cha[3]) + "\n"
                # get author name
                nick = message.author.nick
                if nick is None:
                    nick = message.author.display_name
                emtitle = 'Characters available with name ' + cname
                em = discord.Embed(title=emtitle, description=emdesc, colour=0xfaac41)
                await message.channel.send(msg, embed=em)
            elif len(characters) == 1:
                #   if only one character is found with that name, then add it to the list of tracked characters.
                # search for character ID in userCharacters
                result = db.getOrAddUserCharacters(cname, region, message.author.id)
                # if not found, check ownership and add to list if allowed
                if region is None:
                    region = ''
                if result is True:
                    msg = ('{0.author.mention}, added ' + characterName + ' to the list to track!').format(message)
                elif result is False:
                    msg = ('{0.author.mention}, could not add ' + characterName + ' to the list to track! Please notify a developer.').format(message)
                else:
                    msg = ('{0.author.mention}, ' + characterName + ' is already on the list! Type `!mplus remove ' + cname + ' ' + region + '` to remove.').format(message)
                    #print(result)
                await message.channel.send(msg)
            else:
                # couldn't find it.
                msg = ('{0.author.mention}, could not find that character!').format(message)
                await message.channel.send(msg)
    
    if message.content.startswith('!mplus remove'):
        """not finished"""
        if message.channel.type == discord.ChannelType.private:
            await message.author.send("Mythic Plus Bot cannot respond to some commands in private channels. Try the `remove` command in a Discord Server where this bot has an online presence.")
        else:
            #remove prefix and get character
            characterName = message.content[13:].strip()
            cname = None
            region = None
            if characterName.find(' ') > -1:
                cname = characterName.split(' ')[0]
                region = characterName.split(' ')[1]
            else:
                cname = characterName
            #search for character only within user's account
            #   if multiple characters are found with the same name, ask user to specify which character
            characters = db.findCharacterByName(cname, region)
            msg = None
            if len(characters) > 1:
                msg = ('{0.author.mention}, multiple characters were found with the name `' + characterName + '`. Please specify realm by using the format `character realm`').format(message)
                await message.channel.send(msg)
            elif len(characters) == 1:
                #   if only one character is found with that name, then remove it from the list
                result = db.removeCharacter(cname, region, message.author.id)
                msg = ('{0.author.mention}, removed ' + characterName + ' from the list to track!').format(message)
                await message.channel.send(msg)
            else:
                # couldn't find it.
                msg = ('{0.author.mention}, could not find that character!').format(message)
                await message.channel.send(msg)
    
    if message.content.startswith('!mplus silly'):
        string = message.content[12:].strip()
        string = string[::-1]
        await message.channel.send(string.format(message))
        
    if message.content.startswith('!mplus character list'):
        emdesc = ""
        emtitle = ""
        # reject command from private message
        if message.channel.type == discord.ChannelType.private:
            await message.author.send("Mythic Plus Bot cannot respond to some commands in private channels. Try the `character list` command in a Discord Server where this bot has an online presence.")
        else:
            # get author UID
            uid = message.author.id
            # look in users for bid
            bid = db.getBIDfromDiscordUser(uid)
            # get list of characters belonging to bid
            characterList = db.listAllCharacters(bid)
            # add to list:
            #    character name - realm - level
            for cha in characterList:
                #print(cha)
                emdesc += cha[2] + ' - ' + cha[4] + ' - Level: ' + str(cha[3]) + "\n"
            # get author name
            nick = message.author.nick
            if nick is None:
                nick = message.author.display_name
            emtitle = 'Characters for ' + nick
            em = discord.Embed(title=emtitle, description=emdesc, colour=0xfaac41)
            await message.channel.send("Here's your character list!", embed=em)
    
    if message.content.startswith('!mplus check'):
        if message.channel.type == discord.ChannelType.private:
            await message.author.send("Mythic Plus Bot cannot respond to some commands in private channels. Try the `check` command in a Discord Server where this bot has an online presence.")
        else:
            keys = db.getKeystones()
            emtitle = 'Highest Keystone for Registered Characters'
            emdesc = ''
            for key in keys:
                emdesc += key[0] + ' - ' + key[1] + ' - Keystone Level: ' + key[2] + "\n"
            em = discord.Embed(title=emtitle, description=emdesc, colour=0xfaac41)
            await message.channel.send("Here's the list!", embed=em)
    
    if message.content.startswith('!mplus ping'):
        pingreply = message.content[11:].strip()
        if pingreply == "":
            await message.channel.send("PONG!")
        else:
            await message.channel.send(pingreply)

@client.event
async def on_member_remove(member):
    """
    Find all the characters that belong to this
    member and remove all data.
    """

@client.event
async def on_guild_join(guild):
    # record guild in the database.
    # Any incoming message will have to be verified to see if it is from a registered guild
    gID = guild.id
    db.registerGuild(gID)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    db.configure()

httpserver.bot(client)
httpserver.keep_alive()
client.run(TOKEN)
    
