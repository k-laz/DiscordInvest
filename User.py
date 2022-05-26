class User:
    def __init__(self, id, funds=100000):
        self.id = id
        self.funds = funds
        self.stocks = {}

    # returns the price of purchased stock on success and 0 on failure
    def purchaseStock(self, ticker, shares, quote) -> float:
        if self.cash >= quote:
            if ticker in self.stocks:
                self.stocks[ticker] += shares
            else:
                self.stocks[ticker] = shares
            self.cash -= quote
            #db.add_stock(self.id, ticker, shares)
            return quote
        else:
            return 0
            
    # returns the amount of cash of sold stock on success and 0 on failure
    def sellStock(self, ticker, shares, quote) -> float:
        if self.stocks[ticker] >= shares:
            self.stocks[ticker] -= shares
            self.cash += quote
            #db.sell_stock(self.id, ticker, shares)
            return quote
        else:
            return 0