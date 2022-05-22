from multiprocessing.sharedctypes import Value
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
import logging
import asyncio

from stock import Stock
from DataBase import dataBase


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


#logging.basicConfig(level=logging.INFO)
#TODO: seperate the User class into its own file 
class User:
    def __init__(self, id):
        self.id = id
        self.cash = 100000
        self.stocks = {}

    # returns the price of purchased stock on success and 0 on failure
    def purchaseStock(self, stockName, amount, quote) -> float:
        if self.cash >= quote:
            if stockName in self.stocks:
                self.stocks[stockName] += amount
            else:
                self.stocks[stockName] = amount
            self.cash -= quote
            return quote
        else:
            return 0
            
    # returns the amount of cash of sold stock on success and 0 on failure
    def sellStock(self, ticker, shares, quote) -> float:
        if self.stocks[ticker] >= shares:
            self.stocks[ticker] -= shares
            self.cash += quote
            return quote
        else:
            return 0


bot = commands.Bot(command_prefix='$')
db = dataBase()
stockExchange = Stock()
users = {}

def loadUser(userid) -> User:
    if userid not in users:
        if db.has_account(userid):
            user = User(userid)
            user.cash = db.get_balance(userid)
            stocks = db.get_account_stocks(userid) # stocks is an array of share tuples (ticker, amount) associated with a user 
            for share in stocks:
                user.stocks[share.ticker] = share.amount
            users[userid] = user
        else:
            users[userid] = User(userid)
            db.create_account(userid, 100000) # 100,000 initial mock cash injection
    
    return users[userid]

@bot.event
async def on_ready():
    print('Loading database of users')
    # Load the dictionary from cockroachDB
    print(f'{bot.user.name} has connected to Discord!')



@bot.command(name='invest')
async def invest(ctx):
    await ctx.send(f'{ctx.author}, welcome to your personal mock investment platform')
    await help(ctx)

    user = loadUser(ctx.author.id)

    while True:
        try:
            msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

            if msg.content == "portfolio":
                await show_portfolio(ctx, user)
            elif msg.content == "buy":
                await init_buy(ctx, user)
            elif msg.content == "sell":
                await init_sell(ctx, user)
            elif msg.content == "help":
                await help(ctx)
            elif msg.content == "exit":
                await ctx.send("Leaving Discord Invest...")
                break
            else:
                await ctx.send("Huh?")
        except asyncio.TimeoutError:
            await ctx.send("You took to long...")
            break
    #TODO: save the user to cockroachDB

async def help(ctx):
    await ctx.send('Available commands: portfolio, buy, sell, help, exit')

async def show_portfolio(ctx, user):
    await ctx.send('Your portfolio:')
    await ctx.send(f'CASH: {user.cash}')
    for stock in user.stocks:
        await ctx.send(f'{stock} -> {user.stocks[stock]}')


#TODO: split the buying functionality into seperate function later
async def init_buy(ctx, user):
    await ctx.send("Specify Ticker (ex: TSLA)")

    # flag indicating the user is inputting amount of stock to purchase
    ticker = None
    max_purchase = 0
    while True:
        try:
            # This command waits for either a Ticker or number
            msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

            if msg.content == "exit":
                break
            # msg is the amount of stock to purchase, else its a Ticker
            elif is_number(msg.content) and ticker is not None:
                shares = float(msg.content)
                # quote is the cash needed to purchase specified amount of stock
                #TODO: there is a better way to seperate logic here, a user should not be responsible for handling share calculations
                quote = stockExchange.get_price(ticker, shares)
                buy = user.purchaseStock(ticker, shares, quote)
                if buy == 0:
                    await ctx.send(f'Unable to puchase {shares} shares of {ticker} stock, max purchase is {max_purchase}, try again')
                else:
                    db.add_stock(user.id, ticker, shares)
                    await ctx.send(f'You successfully purchased {shares} shares of {ticker} stock')
                    await ctx.send("Option to buy more: Specify Ticker (ex: TSLA)")
                
            elif stockExchange.validTicker(msg.content):
                ticker = msg.content
                quote = stockExchange.setQuote(ticker)
                max_purchase = stockExchange.maxPurchase(ticker, user.cash)
                await ctx.send(f'Your max buying power of {ticker} is {max_purchase} shares, how much would you like to buy? (input number)')
                
            else:
                await ctx.send("Invalid input, try again...")

        except asyncio.TimeoutError:
            await ctx.send("You took to long...")
            break
    await ctx.send("Leaving exhcange platform...")



async def init_sell(ctx, user):
    await ctx.send("You have the following shares...")
    for share in user.stocks:
        await ctx.send(f'{share} -> {user.stocks[share]}')
    await ctx.send("Specify Ticker (ex: TSLA)")

    # flag indicating the user is inputting amount of stock to purchase
    ticker = None
    max_purchase = 0
    while True:
        try:
            # This command waits for either a Ticker or number
            msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

            if msg.content == "exit":
                break

            # msg is the amount of stock to sell, else its a Ticker
            elif is_number(msg.content) and ticker is not None:
                shares = float(msg.content)
                # quote is the cash returned for specified amount of stock
                quote = stockExchange.get_price(ticker, shares)
                sell = user.sellStock(ticker, shares, quote)
                if sell == 0:
                    await ctx.send(f'Unable to sell {shares} shares of {ticker} stock, you have {user.stocks[ticker]} shares, try again')
                else:
                    db.sell_stock(user.id, ticker, shares)
                    await ctx.send(f'You successfully sold {shares} shares of {ticker} stock for {quote}')
                    await ctx.send("Option to sell more: specify ticker (ex: TSLA)")
                
            #TODO: if user inputs an incorrect Ticker, the validTicker function still returns True for some reason, solve this later
            elif stockExchange.validTicker(msg.content):
                ticker = msg.content
                if ticker in user.stocks:
                    max_sell = stockExchange.maxSell(ticker, user.stocks[ticker])
                    await ctx.send(f'Your max selling power of {user.stocks[ticker]} worth of {ticker} is {max_sell}, how much shares would you like to sell? (Input number)')

            else:
                await ctx.send("Invalid input, try again...")

        except asyncio.TimeoutError:
            await ctx.send("You took to long...")
            break
    await ctx.send("Leaving exhange platform...")
    

def is_number(value):
    try:
        n = float(value)
        return True
    except ValueError:
        return False

bot.run(TOKEN)


