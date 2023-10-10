from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime
from time import sleep


API_KEY = 'PKYM44C7PI5RTRX7LFSG'
API_SECRET = 'cXy7euUOQ1jfXQN8kWUthG4EIHN3uv8CzCPaqngT'
BASE_URL = 'https://paper-api.alpaca.markets'  # use this for paper trading

client = StockHistoricalDataClient(API_KEY,API_SECRET)
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)

symbols = ["F", "GE", "NOK"]

for symbol in symbols:


    bar_request = StockBarsRequest(
        symbol_or_symbols=symbol, 
        timeframe=TimeFrame(1, TimeFrameUnit('Day')), 
        start=datetime(2023, 1, 1), 
        end=datetime(2023, 9, 30), 
        limit=200)
    
    bars = client.get_stock_bars(bar_request)
    print(f"\n\n")
    print(bars[symbol][0])
    print(f"\n\n\n")
    exit()

    short_window = 50
    long_window = 200

    if len(bars) >= long_window:  # Check to ensure we have enough data points
        short_moving_average = sum([bar.open for bar in bars[-short_window:]]) / short_window
        long_moving_average = sum([bar.open for bar in bars[-long_window:]]) / long_window

        try:
            position = trading_client.get_position(symbol)
        except:
            position = None

        if short_moving_average > long_moving_average and not position:
            # Golden Cross - Buy Signal
            trading_client.submit_order(symbol=symbol, qty=10, side='buy', type='market', time_in_force='gtc')
            print(f"Golden Cross detected for {symbol}. Buying 10 shares.")

        elif short_moving_average < long_moving_average and position:
            # Death Cross - Sell Signal
            trading_client.submit_order(symbol=symbol, qty=position.qty, side='sell', type='market', time_in_force='gtc')
            print(f"Death Cross detected for {symbol}. Selling {position.qty} shares.")

account = trading_client.get_account()
for property_name, value in account.__dict__.items():
    print(f"\"{property_name}\": {value}")


