# Work with Python 3.6
import discord
from db import insertUser
import settings as cfg
import wow

TOKEN = cfg.token

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!mplus hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith('!mplus testdb'):
        insertUser(message.author.id, 123456789)
        msg = 'db test finished'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    wow.login()

client.run(TOKEN)