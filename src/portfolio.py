from collections import defaultdict

class Portfolio():
    '''
    Simple portfolio class to manage cash and holdings.
    Args:
        initial_cash (int): Starting cash amount.
    Attributes:
        cash (int): Current cash amount.
        holdings (defaultdict): Dictionary mapping ticker symbols to quantities held.
    Methods:
        tickers_list(): Returns a list of tickers currently in the portfolio.
        sell(ticker, curr_price, quantity): Sells a specified quantity of a ticker at the current price.
        buy(ticker, curr_price, quantity): Buys a specified quantity of a ticker at the current price.
        __str__(): Returns a string representation of the portfolio's cash and holdings.
    '''
    def __init__(self, initial_cash: int):
        self.cash = initial_cash
        self.holdings = defaultdict(int)  # ticker -> quantity

    def tickers_list(self):
        return list(self.holdings.keys()) # maybe more efficient to store list of tickers, add and remove as needed
    
    def sell(self, ticker: str, curr_price: float, quantity: int):
        if ticker in self.holdings and self.holdings[ticker] >= quantity:
            self.holdings[ticker] -= quantity
            self.cash += curr_price * quantity
            if self.holdings[ticker] == 0:
                del self.holdings[ticker]
            print(f"Sold {quantity} of {ticker} at {curr_price}. New cash balance: {self.cash}")
        else:
            print(f"Not enough in holdings to sell {quantity} of {ticker}")
    
    def buy(self, ticker: str, curr_price: float, quantity: int):
        if self.cash >= curr_price * quantity:
            self.holdings[ticker] += quantity
            self.cash -= curr_price * quantity
            print(f"Bought {quantity} of {ticker} at {curr_price}. New cash balance: {self.cash}")
        else:
            print(f"Not enough cash to buy {quantity} of {ticker} at {curr_price}")

    def __str__(self):
        return f"Cash: {self.cash}, Holdings: {self.holdings}"