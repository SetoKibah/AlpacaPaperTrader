from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.requests import OrderRequest
from datetime import datetime, timedelta
from time import sleep


API_KEY = 'PKSOVG2YEBLVPKNA8K5U'
API_SECRET = '09rRznBcGib14PmuAet5ctzhjA6F9vZzCjqEQC71'
BASE_URL = 'https://paper-api.alpaca.markets'  # use this for paper trading

client = StockHistoricalDataClient(API_KEY,API_SECRET)
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
account = trading_client.get_account()

#for property_name, value in account.__dict__.items():
#    print(f"\"{property_name}\": {value}")
#sleep(600)

account = trading_client.get_account()

for property_name, value in account.__dict__.items():
    print(f"\"{property_name}\": {value}")

sleep(300)

symbols = ["F", "GE", "NOK", "MRO", "INST", "IVR", "PLTR", "KEY", "SPOT", "GPRO", "SBUX", "AAPL"]

for symbol in symbols:

    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)    

    bar_request = StockBarsRequest(
        symbol_or_symbols=symbol, 
        timeframe=TimeFrame(1, TimeFrameUnit('Day')), 
        start=start_date, 
        end=end_date, 
        limit=365)
    
    bars = client.get_stock_bars(bar_request)
    """
    print(f"\n\n")
    print(bars[symbol][0])
    print(f"\n\n\n")
    """

    short_window = 50
    long_window = 200
    #print(f'Confirming data point length({len(bars[symbol])}) vs long window({long_window})')
    if len(bars[symbol]) >= long_window:  # Check to ensure we have enough data points
        #print('Data points confirmed...')
        short_moving_average = sum([bar.open for bar in bars[symbol][-short_window:]]) / short_window
        long_moving_average = sum([bar.open for bar in bars[symbol][-long_window:]]) / long_window

        try:
            print(f'Getting {symbol} position...')
            position = trading_client.get_open_position(symbol)
            print(f'Position {symbol} available.')
        except:
            print(f'No position for {symbol}.')
            position = None

        print(f'Short Average: {short_moving_average}\nLong Average: {long_moving_average}')

        if short_moving_average > long_moving_average and not position:
            # Golden Cross - Buy Signal
            print('Buy Signal...')

            # Get current buying power
            current_buying_power = account.__dict__['buying_power']
            print(f'Current Buying Power: {current_buying_power}')
            # Check symbol price
            #print(bars[symbol][-1].timestamp)
            open_price = bars[symbol][-1].open
            #print(f'{symbol} open price {open_price}')
            
            if open_price < current_buying_power:
                # Generate order request object
                order = OrderRequest(
                    symbol=symbol,
                    qty=1,
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )

                trading_client.submit_order(order)
                print(f"Golden Cross detected for {symbol}. Buying 1 share.")
            
            else:
                print(f'Insufficient buying power, we have {current_buying_power} trying to buy {symbol} at {open_price}')


        elif short_moving_average < long_moving_average and position:
            # Death Cross - Sell Signal
            print('Sell Signal...')

            # Generate order request object
            order = OrderRequest(
                symbol=symbol,
                qty=position.qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            
            trading_client.submit_order(order)
            print(f"Death Cross detected for {symbol}. Selling {position.qty} shares.")
        
        else:
            print('No Signals Detected...')
        print('**************************************')
