import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

import logging

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True


# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')

# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print("Bot is ready for use")

@bot.command()
async def ping(context):
    await context.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def buy(ctx):
    await ctx.send(f'Bought this many shares')

bot.run(TOKEN)

# from discord.ext import commands
# bot = commands.Bot(command_prefix='.')

# @bot.event
# async def on_ready():
#     print("Bot is ready for use")

# @bot.command()
# async def ping(context):
#     await context.send(f'Pong! {round(bot.latency * 1000)}ms')

# @bot.command()
# async def buy(ctx):
#     await ctx.send(f'Bought this many shares')

# bot.run(TOKEN)

