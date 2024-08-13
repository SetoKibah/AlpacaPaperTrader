import os
import pandas as pd
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta
from time import sleep
from tqdm import tqdm

# Import credentials from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')

# Initialize clients
client = StockHistoricalDataClient(API_KEY,API_SECRET)
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
account = trading_client.get_account()

# Load the tickers from the CSV file
df = pd.read_csv('tickers.csv')

#print(df.head())
# Initialize counters for uptrend and downtrend stocks
uptrend = 0
downtrend = 0
# Set end date to yesterday
end_date = datetime.now() - timedelta(days=1)
start_date = end_date - timedelta(days=100)

# Iterate over the tickers
for ticker in tqdm(df['Ticker']):
    #print(f'Processing {ticker}...')
    # Get the recent 100 bars of data
    try:
        bar_request = StockBarsRequest(
                symbol_or_symbols=ticker, 
                timeframe=TimeFrame(1, TimeFrameUnit('Day')), 
                start=start_date, 
                end=end_date, 
                limit=100) 
        barset = client.get_stock_bars(bar_request)
        bars = barset[ticker]
        print(f'Bars: {type(bars[0])}')
        sleep(300)
        # Calculate the trend by comparing the latest close price with the average of the last 100 days
    
        close = bars[-1].close
        #print(f'Close: {type(close)}')
        try:
            average = sum([bar.close for bar in bars])/100
        except TypeError as e:
            print(f'Error with {ticker} on {end_date}.')
            print(f'Error: {e}')
            sleep(300)
        if close > average:
            #if ticker == 'PLTR':
            #    print(f'{ticker} is in an uptrend.')
            uptrend += 1
        else:
            #if ticker == 'PLTR':
            #    print(f'{ticker} is in a downtrend.')
            downtrend += 1
    # If there is an error, remove the ticker from the CSV file, 
    # since the error indicates that the ticker is not valid
    except Exception as e:
        print(f'Error with {ticker}.')
        print(f'Error: {e}')
        print('Removing ticker from the csv file...')
        df = df[df['Ticker'] != ticker]
        df.to_csv('tickers.csv', index=False)
        print('Ticker removed.')
        continue


# Print the results
print(f'Uptrend: {uptrend}')
print(f'Downtrend: {downtrend}')