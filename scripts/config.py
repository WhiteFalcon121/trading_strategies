# Universe of tickers
TICKERS = [
    # Tech
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA",
    # Financials
    "JPM", "BAC", "GS",
    # Healthcare
    "JNJ", "PFE", "UNH",
    # Industrials
    "BA", "CAT",
    # Consumer
    "PG", "KO", "DIS", "MCD", "PEP",
    # Energy
    "XOM", "CVX"
]

# Data parameters
DATA_START_DATE = '2015-01-01'
DATA_END_DATE = '2025-01-01'

RAW_DATA_SAVE_PATH = './data/raw/stock_data.csv'

DAYS_12M = 252 # Approx 252 trading days in a year
DAYS_3M = 63  # Approx 63 trading days in 3 months
DAYS_1M = 21  # Approx 21 trading days in a month