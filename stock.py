import os
from typing import Optional

from dotenv import load_dotenv
import finnhub
import re

load_dotenv()


class Stock:
    def __init__(self, ticker):
        self.API_KEY = os.getenv('PROJECT_API_KEY')
        self.finnhub_client = finnhub.Client(api_key=self.API_KEY)
        self.ticker = ticker
        self.quote = self.quote()

    # pattern = '[A-Z]{4,4}'
    # if re.match(pattern, self.ticker):
    # Checks the validity of the ticker and produces a quote for it
    def quote(self) -> Optional[float]:
        symbol_lookup = self.finnhub_client.symbol_lookup(self.ticker)
        if (symbol_lookup.result is not []):
            return self.finnhub_client.quote(symbol_lookup.result[0].symbol['c'])
        else:
            return None


    # returns the max amount of stock user is able to purchase 
    def maxPurchase(self, ticker, cash):
        quote = self.finnhub_client.quote(ticker.upper())
        curPrice = quote['c']
        max_buy = 0
        if curPrice != 0:
            max_buy = cash / curPrice

        return max_buy

    # returns the amount of cash needed to purchase a certain amount of stock
    def get_price(self, ticker, shares):
        quote = self.finnhub_client.quote(ticker.upper())
        curPrice = quote['c']
        cashNeeded = shares*curPrice

        return cashNeeded

    # returns the amount of cash you can get for selling all of your shares in this stock
    def maxSell(self, ticker, shares):
        quote = self.finnhub_client.quote(ticker.upper())
        curPrice = quote['c']
        
        return shares * curPrice

    # returns the amount of 
    def sell(self, amount, stock):
        price = self.finnhub_client.quote(stock.upper())
        curPrice = price['c']
        amountGained = self.__calc(amount, int(curPrice))

        return amountGained
