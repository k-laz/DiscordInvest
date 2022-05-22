import os
import string

from dotenv import load_dotenv
import finnhub

load_dotenv()


class Stock:
    def __init__(self):
        self.API_KEY = os.getenv('PROJECT_API_KEY')
        self.finnhub_client = finnhub.Client(api_key=self.API_KEY)
        self.quote = 0

    def setQuote(self, stock):
        self.quote = self.finnhub_client.quote(stock.upper())

    # returns the max amount of stock user is able to purchase 
    def maxPurchase(self, stock, cash):
        # print(price)
        curPrice = self.quote['c']
        max_buy = 0
        if curPrice != 0:
            max_buy = cash / curPrice

        return max_buy

    # returns the amount of cash needed to purchase a certain amount of stock
    def get_price(self, amount):
        # print(price)
        curPrice = self.quote['c']

        # print('cur - ', curPrice)
        amountNeed = amount*curPrice

        return amountNeed



    def sell(self, amount, stock):
        price = self.finnhub_client.quote(stock.upper())
        curPrice = price['c']
        amountGained = self.__calc(amount, int(curPrice))

        return amountGained

    
    def validTicker(self, stock):
        empty = {'c': 0, 'd': None, 'dp': None, 'h': 0, 'l': 0, 'o': 0, 'pc': 0, 't': 0}
        return self.finnhub_client.quote(stock) is not empty
    