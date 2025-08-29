import yfinance as yf
import pandas as pd
from config import TICKERS, DATA_START_DATE, DATA_END_DATE, RAW_DATA_SAVE_PATH

# tickers = ['AAPL', 'MSFT', 'GOOGL']

data = yf.download(TICKERS, start=DATA_START_DATE, end=DATA_END_DATE, interval='1d')['Close'] # only want close prices
data.to_csv(RAW_DATA_SAVE_PATH)

print(f"Fetched data for tickers: {TICKERS} \n Saved to {RAW_DATA_SAVE_PATH}")