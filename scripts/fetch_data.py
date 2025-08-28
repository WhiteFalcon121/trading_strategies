import yfinance as yf
import pandas as pd

start_date = '2015-01-01'
end_date = '2025-01-01'

tickers = ['AAPL', 'MSFT', 'GOOGL']

save_path = '../data/raw/stock_data.csv'
data = yf.download(tickers, start=start_date, end=end_date, interval='1d')['Close'] # only want close prices
data.to_csv(save_path)

print(f"Fetched data for tickers: {tickers} \n Saved to {save_path}")