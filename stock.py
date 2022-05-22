import os
import string

from dotenv import load_dotenv
import finnhub

load_dotenv()


class stock:

    def __init__(self):
        self.API_KEY = os.getenv('PROJECT_API_KEY')
        self.finnhub_client = finnhub.Client(api_key=self.API_KEY)

    # returns the max amount of stock user is able to purchase 
    def maxPurchase(self, stock, cash):
        # s = stock
        quote = self.finnhub_client.quote(stock.upper())

        # print(price)
        curPrice = quote['c']

        max_buy = cash / curPrice

        return max_buy

    def get_quote(self, stock, amount):
        # s = stock
        quote = self.finnhub_client.quote(stock.upper())

        # print(price)
        curPrice = quote['c']

        # print('cur - ', curPrice)
        amountNeed = self.__calc(amount, int(curPrice))

        return amountNeed



    def sell(self, amount, stock):
        price = self.finnhub_client.quote(stock.upper())
        curPrice = price['c']
        amountGained = self.__calc(amount, int(curPrice))

        return amountGained


    # private method
    def __calc(self, amount, price):

        print('amount - ', amount)
        print('price - ', price)

        self.amountNeeded = amount * price

        return self.amountNeeded
