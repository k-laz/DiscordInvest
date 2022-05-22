import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
import logging
import asyncio

from . import Stock

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#logging.basicConfig(level=logging.INFO)

class User:
    def __init__(self, id):
        self.id = id
        self.cash = 100000
        self.stocks = {}

    # returns the price of purchased stock on success and 0 on failure
    def purchaseStock(self, stockName, amount, quote) -> float:
        if self.cash > quote:
            if stockName in self.stocks:
                self.stocks[stockName] += amount
            else:
                self.stocks[stockName] = amount
            self.cash -= quote
            return quote
        else:
            return 0
            
    # def portfolio(self):
    #     return [self.cash, self.stocks]
        


bot = commands.Bot(command_prefix='$')
users = {}

def loadUser(userid) -> User:
    if userid not in users:
        users[userid] = User(userid)
    
    return users[userid]

@bot.event
async def on_ready():
    print('Loading database of users')
    # Load the dictionary from cockroachDB
    print(f'{bot.user.name} has connected to Discord!')



@bot.command(name='invest')
async def invest(ctx):
    await ctx.send(f'{ctx.author}, welcome to your personal mock investment platform')
    await ctx.send('Available commands: portfolio, buy, sell, help, exit')
    user = loadUser(ctx.author.id)

    while True:
        try:
            msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

            if msg.content == "portfolio":
                await show_portfolio(ctx, user)
            elif msg.content == "buy":
                await init_buy(ctx, user)
            elif msg.content == "exit":
                await ctx.send("leaving platform...")
                break
            else:
                await ctx.send("Huh?")

        except asyncio.TimeoutError:
            await ctx.send("You took to long...")
            break


async def show_portfolio(ctx, user):
    await ctx.send('Your portfolio:')
    await ctx.send(f'Cash: {user.cash}')
    for stock in user.stocks:
        await ctx.send(f'{stock} - {user.stocks[stock]}')

async def init_buy(ctx, user):
    await ctx.send("Specify Ticker (ex: TSLA)")

    # flag indicating the user is inputting amount of stock to purchase
    ticker = None
    while True:
        try:
            # This command waits for either a Ticker or number
            msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

            # msg is the amount of stock to purchase, else its a Ticker
            if is_number(msg) and ticker is not None:
                # quote is the amount of cash needed to purchase specified amount of stock
                quote = Stock.get_quote(ticker, msg)
                user.purchase_stock(ticker, msg, quote)
                    
            elif Stock.validTicker(msg):
                ticker = msg
                max_purchase = await Stock.maxPurchase(msg, user.cash)
                await ctx.send(f'Your max buying power of {msg} is {max_purchase}, how much would you like to buy? (input number)')
                continue
            else:
                await ctx.send("Invalid input, try again...")
                continue

        except asyncio.TimeoutError:
            await ctx.send("You took to long...")
            break

def is_number(value):
    return type(value) in [int, float]

bot.run(TOKEN)


