import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#logging.basicConfig(level=logging.INFO)

class User:
    def __init__(self, id):
        self.id = id
        self.cash = 100000
        self.stocks = {}

    def purchaseStock(self, stockName, amount):
        if stockName in self.stocks:
            self.stocks[stockName] += amount
        else:
            self.stocks[stockName] = amount
        


bot = commands.Bot(command_prefix='$')

users = {}

@bot.event
async def on_ready():
    print('Loading database of users')
    # Load the dictionary from cockroachDB
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='invest')
async def invest(ctx):
    #await ctx.send(ctx.author)
    userid = ctx.author.id
    
    if userid not in users:
        user = User(ctx.author.id)
        users[userid] = user
    else:
        user = users[userid]

    user.purchaseStock('TSLA', 123)

    x = user.stocks.get('TSLA')
    await ctx.send(f'you just purchased {x} of TSLA')



bot.run(TOKEN)


