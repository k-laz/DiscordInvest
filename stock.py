import os
import string

from dotenv import load_dotenv
import finnhub

load_dotenv()


class Stock:
    def __init__(self):
        self.API_KEY = os.getenv('PROJECT_API_KEY')
        self.finnhub_client = finnhub.Client(api_key=self.API_KEY)

    def setQuote(self, stock):
        self.quote = self.finnhub_client.quote(stock.upper())

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


    def sell(self, amount, stock):
        price = self.finnhub_client.quote(stock.upper())
        curPrice = price['c']
        amountGained = self.__calc(amount, int(curPrice))

        return amountGained

    
    #TODO: add correct regex here to test for TSLA 
    def validTicker(self, stock):
        empty = {'c': 0, 'd': None, 'dp': None, 'h': 0, 'l': 0, 'o': 0, 'pc': 0, 't': 0}
        return self.finnhub_client.quote(stock) is not empty
    