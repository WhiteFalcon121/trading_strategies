import pandas as pd
from src.portfolio import Portfolio
from scripts.config import DAYS_12M, DAYS_3M, DAYS_1M
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller

# CHANGE portfolio to pf (parameter)
def momentum_strategy(prices: pd.DataFrame, portfolio: Portfolio, rebalance_freq: int) -> None:
    '''
    Implements relative momentum strategy.
    
    Args:
        prices (pd.DataFrame): DataFrame with dates as index and tickers as columns, containing closing price data.
        portfolio (Portfolio): Portfolio object to manage cash and holdings.
        rebalance_freq (int): Frequency of rebalancing in days.
    Returns:
        None: The function modifies the portfolio in place.
    '''
    # precompute returns
    returns = [prices.pct_change(periods=DAYS_12M), prices.pct_change(periods=DAYS_3M), prices.pct_change(periods=DAYS_1M)]

    rebalance_dates = (returns[0].index[DAYS_12M::rebalance_freq]) # rebalancing dates (every month after first 12 months) ] now a parameter

    # for each date, rank stocks based on returns
    for date in rebalance_dates:
        # calculate momentum scores

        latest_z_scores = [] # list to hold latest z scores for each ticker, for each period (index 0 is 12m, 1 is 3m, 2 is 1m)

        for period in returns:
            latest_returns = period.loc[date] # to get specific date's returns
            latest_mean = latest_returns.mean() # mean of last row
            latest_std = latest_returns.std() # std of last row
            latest_z = (latest_returns - latest_mean) / latest_std
            latest_z = latest_z.dropna() # drop NaNs (extra safe)
            latest_z_scores.append(latest_z)
        momentum_scores = (0.5 * latest_z_scores[0]) + (0.3 * latest_z_scores[1]) + (0.2 * latest_z_scores[2])

        ranked_stocks = (momentum_scores.sort_values(ascending=False)[:10]).index.tolist() # top 10 momentum stocks

        '''
        # trading logic (adjust incrementally)

        # sell stocks not in ranked_stocks
        for ticker in portfolio.tickers_list():
            if ticker not in ranked_stocks:
                # sell logic
                curr_price = prices.loc[date, ticker]
                quantity = portfolio.holdings[ticker]
                portfolio.sell(ticker, curr_price, quantity)
                print(f"Sold all holdings of {ticker} at {curr_price}")

        stocks_to_buy = [ticker for ticker in ranked_stocks if ticker not in portfolio.holdings]
        cash_per_stock = (portfolio.cash // len(stocks_to_buy)) if stocks_to_buy else 0 # equal weighting
        if cash_per_stock == 0:
            print("No cash available to buy new stocks.")
            continue

        # buy ranked_stocks
        for ticker in stocks_to_buy:
            # buy logic
            curr_price = prices.loc[date, ticker] # need to make this THE NEXT DAY
            quantity = cash_per_stock // curr_price
            if quantity > 0:
                portfolio.buy(ticker, curr_price, quantity)
            else:
                print(f"Not enough cash to buy {quantity} shares of {ticker} at {curr_price}")

        # print(portfolio.tickers_list())
        '''

        # trading logic (full rebalance) - less path-dependent so more academically accurate
        
        # sell all stocks at today's close
        for ticker in portfolio.tickers_list():
            curr_price = prices.loc[date, ticker]
            quantity = portfolio.holdings[ticker]
            portfolio.sell(ticker, curr_price, quantity)
            print(f"Sold all holdings of {ticker} at {curr_price}")
        
        # buy ranked_stocks at next day's close
        cash_per_stock = (portfolio.cash // len(ranked_stocks)) if ranked_stocks else 0 # equal weighting
        if cash_per_stock == 0:
            print("No cash available to buy new stocks.")
            continue
        else:
            next_day_index = prices.index.get_loc(date) + 1
            if next_day_index >= len(prices.index):
                print(f"No next day data available for {date}. Skipping buy.")
                continue
            for ticker in ranked_stocks:
                # use next day's price to sell
                next_day = prices.index[next_day_index]
                next_day_price = prices.loc[next_day, ticker]
                quantity = cash_per_stock // next_day_price
                if quantity > 0:
                    portfolio.buy(ticker, next_day_price, quantity)
                else:
                    print(f"Not enough cash to buy {quantity} shares of {ticker} at {next_day_price}")

        # save portfolio value
        portfolio.save_value(next_day, prices.loc[next_day].to_dict())

def pairs_strategy(prices: pd.DataFrame, portfolio: Portfolio, ticker_A: str, ticker_B: str) -> None:
    price_window = prices[[ticker_A, ticker_B]].loc['2017-01-03':'2017-04-28']
    # ticker_A, ticker_B = 'XOM', 'CVX' # pair chosen
    prices_A, prices_B = price_window[ticker_A], price_window[ticker_B] # just price levels

    # if linear combination of 2 price levels is stationary, likely good candidates
    # so cointegration test, p-value < 0.05 typically indicates cointegration
    _, coint_p_value, _ = coint(prices_A, prices_B)
    print(f'Cointegration test p-value: {coint_p_value}')
    if coint_p_value >= 0.05:
        print("Pair not likely to be good fit - aborted strategy.")
        return
    
    X = sm.add_constant(prices_B) # add column of 1s for intercept
    model = sm.OLS(prices_A, X).fit() # ordinary least squares regression
    alpha, beta = model.params
    print(f'Alpha: {alpha}, Beta: {beta}')

    trade_window = prices[[ticker_A, ticker_B]].loc['2018-11-01': '2019-04-30'] # using different timeframe to test strategy
    spread = trade_window[ticker_A] - alpha - beta * trade_window[ticker_B] # rearranging formula to make residual (the spread) the subject

    # adf_result = adfuller(spread)
    # adf_p_value = adf_result[1]
    # print(f"adfuller p-value: {adf_p_value}")
    # if adf_p_value >= 0.05:
    #     print("Spread likely not mean reverting.")
    #     return

    z_scores: pd.Series = (spread - spread.mean()) / spread.std()    
    dates = trade_window.index

    for date in dates:
        price_A = trade_window.loc[date][ticker_A]
        price_B = trade_window.loc[date][ticker_B]
        # CHANGE ACTIONS TO NEXT DAY PRICES LATER
        z_score = z_scores[date]
        if z_score > 2:
            print(f"{date}: Short A, Long B")
            quantity_A = portfolio.cash // (price_A + abs(beta) * price_B)
            quantity_B = abs(beta) * quantity_A # else make it 0
            portfolio.short(ticker_A, price_A, quantity_A)
            portfolio.buy(ticker_B, price_B, quantity_B)
        elif z_score < -2:
            print(f"Day {date}: Long A, Short B")
            quantity_A = abs(beta) * quantity_B # else make it 0
            quantity_B = portfolio.cash // (price_B + abs(beta) * price_A)
            portfolio.buy(ticker_A, price_A, quantity_A)
            portfolio.short(ticker_B, price_B, quantity_B)
        elif z_score < 0.5:
            print(f"Day {date}: Close positions")
            if portfolio.shortings[ticker_A] > 0:
                portfolio.cover(ticker_A, price_A, portfolio.shortings[ticker_A])
            elif portfolio.holdings[ticker_A] > 0:
                portfolio.sell(ticker_A, price_A, portfolio.holdings[ticker_A])

            if portfolio.shortings[ticker_B] > 0:
                portfolio.cover(ticker_B, price_B, portfolio.shortings[ticker_B])
            elif portfolio.holdings[ticker_B] > 0:
                portfolio.sell(ticker_B, price_B, portfolio.holdings[ticker_B])
        else:
            print(f"Day {date}: Hold positions")
            continue

        portfolio.save_value(date, prices.loc[date].to_dict())
    