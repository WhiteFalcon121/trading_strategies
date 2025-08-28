import yfinance as yf
import pandas as pd
from config import TICKERS, START_DATE, END_DATE, RAW_DATA_SAVE_PATH

# tickers = ['AAPL', 'MSFT', 'GOOGL']

data = yf.download(TICKERS, start=START_DATE, end=END_DATE, interval='1d')['Close'] # only want close prices
data.to_csv(RAW_DATA_SAVE_PATH)

print(f"Fetched data for tickers: {TICKERS} \n Saved to {RAW_DATA_SAVE_PATH}")