import pandas as pd

# Trading day constants - move later to config
DAYS_12M = 252 # Approx 252 trading days in a year
DAYS_3M = 63  # Approx 63 trading days in 3 months
DAYS_1M = 21  # Approx 21 trading days in a month

def momentum_strategy(prices: pd.DataFrame):
    # precompute returns
    returns = [prices.pct_change(periods=DAYS_12M), prices.pct_change(periods=DAYS_3M), prices.pct_change(periods=DAYS_1M)]

    rebalance_dates = (returns[0].index[DAYS_12M::DAYS_1M]) # rebalancing dates (every month after first 12 months)

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

        ranked_stocks = momentum_scores.sort_values(ascending=False)[:10] # top 10 momentum stocks

        # TODO: implement trading logic
        # sell stocks not in ranked_stocks
        # buy ranked_stocks