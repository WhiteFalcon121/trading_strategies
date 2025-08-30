from src.portfolio import Portfolio
from src.signals import momentum_strategy
import pandas as pd
from scripts.config import DAYS_1M

def main():
    initial_cash = 100000  # Starting with $100,000
    transaction_cost = 0.001  # 0.1% transaction cost
    slippage = 0.001  # 0.1% slippage
    portfolio = Portfolio(initial_cash, transaction_cost + slippage)

    prices = pd.read_csv('data/raw/stock_data.csv')
    prices.set_index('Date', inplace=True)

    momentum_strategy(prices, portfolio, DAYS_1M)
    # print("Portfolio value history: ", portfolio.value_history)
    print(f"Final portfolio value: {portfolio.get_current_value(prices.iloc[-1].to_dict())}")
    print(f"CAGR: {portfolio.cagr()}")
    print(f"Volatility: {portfolio.volatility()}")
    print(f"Sharpe: {portfolio.sharpe()}")

if __name__ == "__main__":
    main()