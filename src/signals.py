import pandas as pd
from src.portfolio import Portfolio
from scripts.config import DAYS_12M, DAYS_3M, DAYS_1M

def momentum_strategy(prices: pd.DataFrame, portfolio: Portfolio, rebalance_dates: list):
    '''
    Implements relative momentum strategy.
    
    Args:
        prices (pd.DataFrame): DataFrame with dates as index and tickers as columns, containing closing price data.
        portfolio (Portfolio): Portfolio object to manage cash and holdings.
        rebalance_dates (list): List of dates (as strings) on which to rebalance the portfolio.
    Returns:
        None: The function modifies the portfolio in place.
    '''
    # precompute returns
    returns = [prices.pct_change(periods=DAYS_12M), prices.pct_change(periods=DAYS_3M), prices.pct_change(periods=DAYS_1M)]

    # rebalance_dates = (returns[0].index[DAYS_12M::DAYS_1M]) # rebalancing dates (every month after first 12 months) ] now a parameter

    # for each date, rank stocks based on returns
    for date in rebalance_dates:
        # calculate momentum scores

        latest_z_scores = [] # list to hold latest z scores for each ticker, for each period (index 0 is 12m, 1 is 3m, 2 is 1m)

        for period in returns:
            latest_returns = period.loc[date] # to get specific date's returns
            latest_mean = latest_returns.mean() # mean of last row
            latest_std = latest_returns.std() # std of last row
            latest_z_scores.append((latest_returns - latest_mean) / latest_std)
        momentum_scores = (0.5 * latest_z_scores[0]) + (0.3 * latest_z_scores[1]) + (0.2 * latest_z_scores[2])

        ranked_stocks = (momentum_scores.sort_values(ascending=False)[:10]).index.tolist() # top 10 momentum stocks

        # trading logic (adjust incrementally)
        stocks_to_buy_num = 0

        # sell stocks not in ranked_stocks
        for ticker in portfolio.tickers_list():
            if ticker not in ranked_stocks:
                # sell logic
                curr_price = prices.loc[date, ticker]
                quantity = portfolio.holdings[ticker]
                portfolio.sell(ticker, curr_price, quantity)
                stocks_to_buy_num += 1

        cash_per_stock = portfolio.cash // stocks_to_buy_num if stocks_to_buy_num > 0 else 0 # equal weighting
        
        # buy ranked_stocks
        for ticker in ranked_stocks:
            if ticker not in portfolio.holdings:
                # buy logic
                curr_price = prices.loc[date, ticker]
                quantity = cash_per_stock // curr_price
                if quantity > 0:
                    portfolio.buy(ticker, curr_price, quantity)
                    portfolio.holdings[ticker] += quantity
                else:
                    print(f"Not enough cash to buy any shares of {ticker} at {curr_price}")