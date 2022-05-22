import os
import string

from dotenv import load_dotenv
import finnhub

load_dotenv()


class stock:

    def __init__(self):
        self.API_KEY = "sandbox_ca4pl4aad3ibhjmjp4hg"
        self.finnhub_client = finnhub.Client(api_key=self.API_KEY)

    def buy(self, amount, stock):
        # s = stock
        price = self.finnhub_client.quote(stock.upper())

        # print(price)

        curPrice = price['c']

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
