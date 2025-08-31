from scripts.fetch_data import fetch_data
from scripts.backtest import run_backtest
import pandas as pd

if __name__ == "__main__":
    fetch_data()
    prices = pd.read_csv('data/raw/stock_data.csv')
    prices.set_index('Date', inplace=True)
    run_backtest(prices)