from collections import defaultdict
import pandas as pd
from scripts.config import DAYS_1M, DAYS_12M

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
    def __init__(self, initial_cash: int, transaction_cost: float):
        self.cash = initial_cash
        self.holdings = defaultdict(int)  # ticker -> quantity
        self.trade_cost = transaction_cost  # 0.1% transaction cost
        self.value_history = pd.Series()  # to track portfolio value over time

    def tickers_list(self):
        return list(self.holdings.keys()) # maybe more efficient to store list of tickers, add and remove as needed

    def get_current_value(self, prices: dict):
        total_value = self.cash
        for ticker, quantity in self.holdings.items():
            if ticker in prices:
                total_value += prices[ticker] * quantity
        return total_value

    def save_value(self, date: str, prices: dict):
        current_value = self.get_current_value(prices)
        self.value_history[date] = current_value

    def sell(self, ticker: str, curr_price: float, quantity: int):
        if ticker in self.holdings and self.holdings[ticker] >= quantity:
            self.holdings[ticker] -= quantity
            self.cash += (1 - self.trade_cost) * (curr_price * quantity)
            if self.holdings[ticker] == 0:
                del self.holdings[ticker]
            print(f"Sold {quantity} of {ticker} at {curr_price}. New cash balance: {self.cash}")
        else:
            print(f"Not enough in holdings to sell {quantity} of {ticker}")
    
    def buy(self, ticker: str, curr_price: float, quantity: int):
        net_cost = (1 + self.trade_cost) * (curr_price * quantity)
        if self.cash >= net_cost:
            self.holdings[ticker] += quantity
            self.cash -= net_cost
            print(f"Bought {quantity} of {ticker} at {curr_price}. New cash balance: {self.cash}")
        else:
            print(f"Not enough cash to buy {quantity} of {ticker} at {curr_price}")

    # metrics

    def cagr(self):
        if self.value_history.empty:
            print("No value history to calculate CAGR.")
            return None
        elif len(self.value_history) < 2:
            print("Not enough data points in value history to calculate CAGR.")
            return None
        start_date, end_date = self.value_history.index[0], self.value_history.index[-1]
        # print(start_date, end_date)
        start_value, end_value = self.value_history.iloc[0], self.value_history.iloc[-1]
        num_years = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days / 365.25
        return (end_value / start_value) ** (1 / num_years) - 1
    
    def volatility(self):
        if self.value_history.empty:
            print("No value history to calculate volatility.")
            return None
        returns = self.value_history.pct_change().dropna()
        return returns.std() * ((DAYS_12M/DAYS_1M) ** 0.5)