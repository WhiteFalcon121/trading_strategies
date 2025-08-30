from src.portfolio import Portfolio
from src.signals import momentum_strategy
import pandas as pd
from scripts.config import DAYS_1M
import matplotlib.pyplot as plt

def run_backtest():
    initial_cash = 100000  # Starting with $100,000
    transaction_cost = 0.001  # 0.1% transaction cost
    slippage = 0.001  # 0.1% slippage
    portfolio = Portfolio(initial_cash, transaction_cost + slippage)
    prices = pd.read_csv('data/raw/stock_data.csv')
    prices.set_index('Date', inplace=True)

    momentum_strategy(prices, portfolio, DAYS_1M)
    print("\n")
    print(f"Final portfolio value: {portfolio.get_current_value(prices.iloc[-1].to_dict())}")
    # print(f"CAGR: {portfolio.cagr()}")
    # print(f"Volatility: {portfolio.volatility()}")
    # print(f"Sharpe: {portfolio.sharpe()}")
    portfolio_stats = pd.Series([portfolio.cagr(), portfolio.volatility(), portfolio.sharpe()], index=['CAGR', 'Volatility', 'Sharpe'])
    portfolio_stats.to_csv('results/portfolio_stats.csv')
    portfolio.value_history.plot(title="Portfolio Value Over Time")
    portfolio.value_history.to_csv('data/processed/portfolio_value_history.csv')
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.grid()
    # plt.show()
    plt.savefig('results/portfolio_value_over_time.png')