import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)



# bot = commands.Bot(command_prefix='.')

# @bot.event
# async def on_ready():
#     print("Bot is ready for use")

# @bot.event
# async def on_member_join(member):
#     print(f'{member} has joined the server.')

# @bot.event
# async def on_member_remove(member):
#     print(f'{member} has been removed!')
