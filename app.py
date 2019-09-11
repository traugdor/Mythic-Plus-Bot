# Work with Python 3.6
import discord

import db
import settings as cfg
import wow

TOKEN = cfg.token

client = discord.Client()
from httpserver import keep_alive, bot

bot(client)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!mplus hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!mplus testdb'):
        db.insertWowCharacter(1, "Myorga", "wyrmrest-accord")
        msg = 'db test finished'.format(message)
        await client.send_message(message.channel, msg)
        
    if message.content.startswith('!mplus register'):
        """not implemented"""
        #get user id
        #generate URL and use it as part of the unique state id
        registermessage = " \
        Thank you for choosing Mythic Plus Bot! Click this link to get going! \
        \
        " + cfg.botBaseUrl + "?url=https%3A%2F%2Fus.battle.net%2Foauth%2Fauthorize%3Fscope%3Dwow.profile%26client_id%3D" \
        + cfg.wowClientId + "%26state%3DUID" + str(message.author.id) \
        + "%26redirect_uri%3Dhttps%3A%2F%2F93010e781ce7453389bdac92f444797d.vfs.cloud9.us-east-2.amazonaws.com%2Foauth%2Fcallback%26response_type%3Dcode"
        try:
            await client.send_message(message.author, registermessage)
        except discord.errors.Forbidden:
            await client.send_message(message.channel, "{0.author.mention}, I can't send you a direct message! \n\n \
 \
Please allow members of this Discord Server to send you a direct message to continue. \n\n \
 \
To do this, click on the `v` by the server name up top and choose \"Privacy Settings\" from the menu. \n \
Then in the window that pops up, move the slider to the right beside \"Allow direct messages from server members\" and try again.".format(message))
        
    if message.content.startswith('!mplus add'):
        #remove prefix and only select the character name.
        characterName = message.content[10:].strip()
        #search for character only within user's account
        #   if multiple characters are found with the same name, ask user to specify which character
        msg = ('{0.author.mention}, multiple characters were found with that name ' + characterName + '. Please specify region.').format(message)
        await client.send_message(message.channel, msg)
        #   if only one character is found with that name, then add it to the list of tracked characters.
        msg = ('{0.author.mention}, added ' + characterName + ' to the list to track!').format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!mplus silly'):
        string = message.content[12:].strip()
        string = string[::-1]
        await client.send_message(message.channel, string.format(message))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    db.configure()

keep_alive()
client.run(TOKEN)
    
