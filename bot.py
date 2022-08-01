from multiprocessing.sharedctypes import Value
import os
from turtle import color

import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

from Stock import Stock
from User import User
from Embed import Embed

import config

import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix=':')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# -----------------------------------------------------------------------------------------
# TRANSACTION COMMANDS
# -----------------------------------------------------------------------------------------
@bot.command(name="buy", description="Buy a stock.")
async def buy_stock(
    ctx,
    ticker: discord.Option(str, "Enter a stock ticker"),
    quantity
    # ctx: discord.ApplicationContext,
    
    # quantity: discord.Option(float, "Enter desired quantity to buy")
    ):

    user = User(str(ctx.author.id), str(ctx.author))
    ticker = ticker.upper()
    stock = Stock(ticker)
    
    if(stock.quote is None):
        await ctx.respond(f"Could not find {ticker}. Please try again.")
    else:
        fields = [
            ["Order Type", "Market Buy"],
            ["Asset Price", f"${stock.quote:.2f}"],
            ["Quantity", quantity], 
            ["Order Total", f"${(quantity * stock.quote):.2f}"],
            ["Available Funds", f"${user.funds:.2f}"]
        ]
        
        await ctx.send(embed=Embed(author=stock.exchange,title=ticker,fields=fields, color=discord.Color.green))

        # view = ConfirmButtons(symbol, quantity, True, ctx, player)
        # await ctx.respond(embed=embedded_message(
        #     status='pending',
        #     author=query.exchange,
        #     thumbnail=thumbnail_url,
        #     title=symbol,
        #     desc=query.name,
        #     fields=fields_list,
        #     footer_text="Order Status: Pending",
        #     colour=0xEEB902), view=view)

bot.run(TOKEN)


