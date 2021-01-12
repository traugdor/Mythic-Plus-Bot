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
    
    print(message.author.name + ": " + message.content)

    if message.content.startswith('!mplus hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
        
    if message.content.startswith('!mplus register'):
        #get user id
        #generate URL and use it as part of the unique state id
        registermessage = " \
        Thank you for choosing Mythic Plus Bot! Click this link to get going! \
        \
        " + cfg.botBaseUrl + "?url=https%3A%2F%2Fus.battle.net%2Foauth%2Fauthorize%3Fscope%3Dwow.profile%26client_id%3D" \
        + cfg.wowClientId + "%26state%3DUID" + str(message.author.id) \
        + "%26redirect_uri%3Dhttps%3A%2F%2F93010e781ce7453389bdac92f444797d.vfs.cloud9.us-east-2.amazonaws.com%2Foauth%2Fcallback%26response_type%3Dcode"
        try:
            await message.author.send(registermessage)
        except discord.errors.Forbidden:
            await message.channel.send("{0.author.mention}, I can't send you a direct message! \n\n \
 \
Please allow members of this Discord Server to send you a direct message to continue. \n\n \
 \
To do this, click on the `v` by the server name up top and choose \"Privacy Settings\" from the menu. \n \
Then in the window that pops up, move the slider to the right beside \"Allow direct messages from server members\" and try again.".format(message))
        
    if message.content.startswith('!mplus add'):
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
            msg = ('{0.author.mention}, multiple characters were found with the name `' + characterName + '`. Please specify realm by using the format `character realm`').format(message)
            await message.channel.send(msg)
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
        keys = db.getKeystones()
        emtitle = 'Highest Keystone for Registered Characters'
        emdesc = ''
        for key in keys:
            emdesc += key[0] + ' - ' + key[1] + ' - Keystone Level: ' + key[2] + "\n"
        em = discord.Embed(title=emtitle, description=emdesc, colour=0xfaac41)
        await message.channel.send("Here's the list!", embed=em)

@client.event
async def on_member_remove(member):
    """
    Find all the characters that belong to this
    member and remove all data.
    """

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    db.configure()
    
async def find_channel(guild):
    """
    Finds a suitable guild channel for posting the
    welcome message.
    """
    for c in guild.channels:
        if not c.permissions_for(guild.me).send_messages:
            continue
        return c

httpserver.keep_alive()
client.run(TOKEN)
    
