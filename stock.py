import os

from dotenv import load_dotenv
import finnhub
import re

load_dotenv()


class Stock:
    def __init__(self):
        self.API_KEY = os.getenv('PROJECT_API_KEY')
        self.finnhub_client = finnhub.Client(api_key=self.API_KEY)

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

    
    #TODO: add correct matching for existing stock tickers, needs more research
    def validTicker(self, ticker):
        pattern = '[A-Z]{4,4}'
        result = re.match(pattern, ticker)
        return result
        # if result:
        #     print(self.finnhub_client.symbol_lookup(ticker))
        #     return True
        # return False