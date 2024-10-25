import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'hello':
        await message.channel.send(f'Hello, {message.author.name}!')

client.run(os.getenv('MTI5ODg4NzE3Mjg0OTQwMTg3Nw.GgTkkW.ykNC0VFB6Ac8FktVm62DnmvvmQ6VwqV26LME2M'))
requests aiohttp
