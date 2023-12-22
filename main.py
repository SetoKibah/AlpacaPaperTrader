from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.requests import OrderRequest
from datetime import datetime, timedelta
import sqlite3
from time import sleep


API_KEY = 'PKSOVG2YEBLVPKNA8K5U'
API_SECRET = '09rRznBcGib14PmuAet5ctzhjA6F9vZzCjqEQC71'
BASE_URL = 'https://paper-api.alpaca.markets'  # use this for paper trading

# Constants
take_profit = 0.05
stop_loss = -0.05

# Initialize clients
client = StockHistoricalDataClient(API_KEY,API_SECRET)
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
account = trading_client.get_account()


# Connect to database and create table if it doesn't exist
conn = sqlite3.connect('frozen_symbols.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS frozen_symbols (symbol TEXT PRIMARY KEY, time TEXT)')
conn.commit()
conn.close()



# List of symbols to trade
symbols = ["F", "GE", "NOK", "MRO", "INST", "IVR", "PLTR", "KEY", "SPOT", "GPRO", "SBUX", "AAPL",
           "KR", "BAC","SIFY", "FPAY", "CAN", "GSAT", "LUMN", "API", "IHRT", "MVIS", "VMEO", "KODK",
           "UIS", "YEXT", "PTON", "T", "NIO", "TSLA", "AMZN", "MSFT", "META", "GOOG", "GOOGL", "CLNN",
           "OMQS", "SDPI", "CLRO", "PRPL", "CODX", "PFIE", "COOK", "SPWH", "SERA", "CLAR", "LFVN", "CRCT",
           "BRDG", "HCAT", "SNFCA", "RXRX", "DOMO", "CLSK", "TRAK", "NATR", "NUS", "MYGN", "VREX", "BYON",
           "PRG", "FC", "ZION", "SKYW", "USNA", "HQY", "MMSI", "UTMD", "IIPR", "EXR"]

# Function to add a symbol to the frozen symbols database
def freeze_symbol(symbol, time):
    # Connect to database
    conn = sqlite3.connect('frozen_symbols.db')
    c = conn.cursor()

    # Add the frozen symbols to the database
    c.execute('INSERT OR REPLACE INTO frozen_symbols VALUES (?, ?)', (symbol, time.strftime('%Y-%m-%d %H:%M:%S.%f')))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Function to check if a symbol is frozen
def is_symbol_frozen(symbol):
    # Connect to database
    conn = sqlite3.connect('frozen_symbols.db')
    c = conn.cursor()

    # Query the database for the symbol
    c.execute('SELECT * FROM frozen_symbols WHERE symbol=?', (symbol,))
    
    # If the symbol is in the database, return the time
    result = c.fetchone()
    # If symbol is not in the database, return False
    if result is None:
        result = False
    
    # Close connection
    conn.close()

    return result

# Function to calculate the moving average
def moving_average(lst, window_size):
    moving_averages = []
    window_sum = sum(lst[:window_size])
    moving_averages.append(window_sum / window_size)

    for i in range(window_size, len(lst)):
        window_sum = window_sum - lst[i - window_size] + lst[i]
        moving_averages.append(window_sum / window_size)

    return moving_averages

# Function to calculate the quantity of shares to buy
def calculate_quantity(current_buying_power, open_price):
    quantity = int(current_buying_power / open_price)
    if quantity > 5:
        print(f'Quantiy is {quantity}, reducing to 5 shares.')
        quantity = 5
    return quantity

# Function to create a buy order request
def create_buy_order(symbol, quantity):
    return OrderRequest(
        symbol=symbol,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='gtc'
    )


def main():
    
    for symbol in symbols:

        # Check if symbol is frozen and when it was frozen
        if is_symbol_frozen(symbol):
            frozen_time = is_symbol_frozen(symbol)
            # Check if symbol has been frozen for more than 5 days
            if datetime.now() - datetime.strptime(frozen_time[1], '%Y-%m-%d %H:%M:%S.%f') > timedelta(days=5):                
                print(f'{symbol} has been frozen for more than 5 days, removing from frozen list.')
                # Remove symbol from frozen database
                conn = sqlite3.connect('frozen_symbols.db')
                c = conn.cursor()
                c.execute('DELETE FROM frozen_symbols WHERE symbol=?', (symbol,))
                conn.commit()
                conn.close()
            
            else:
                print(f'{symbol} is frozen, skipping...')
                continue

        # Update account information
        account = trading_client.get_account()
        print(f"Current Buying Power: ${account.__dict__['buying_power']}")

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
            short_moving_average = moving_average([bar.open for bar in bars[symbol]], short_window)[-1]
            long_moving_average = moving_average([bar.open for bar in bars[symbol]], long_window)[-1]
            print('Moving averages calculated...')

            # Display the signal generated by the moving averages
            print('Stock is currently trading at: $' + str(bars[symbol][-1].open))
            # Display the resulting deatch cross or golden cross signal
            if short_moving_average > long_moving_average:
                print('Golden Cross')
            elif short_moving_average < long_moving_average:
                print('Death Cross')
            else:
                print('No Signal')
            

            try:
                print(f'Getting {symbol} position...')
                position = trading_client.get_open_position(symbol)
                print(f'Position {symbol} available.')
                # Display current position return percentage
                percent_return = round(float(position.unrealized_plpc), 3)
                print(f'Current Position Return: {percent_return}%')
            except:
                print(f'No position for {symbol}.')
                percent_return = 0
                position = None

            print(f'Short Average: {short_moving_average}\nLong Average: {long_moving_average}')
            
            if percent_return < stop_loss and position:
                # Stop Loss - Sell Signal
                print('Stop Loss...')

                # Generate order request object
                order = OrderRequest(
                    symbol=symbol,
                    qty=position.qty,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
                
                trading_client.submit_order(order)

                # Add symbol and time to frozen symbols
                freeze_symbol(symbol, datetime.now())

                print(f"Stop Loss detected for {symbol}. Selling {position.qty} shares.")
            
            elif percent_return > take_profit and position:
                # Take Profit - Sell Signal
                print('Take Profit...')

                # Generate order request object
                order = OrderRequest(
                    symbol=symbol,
                    qty=position.qty,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
                
                trading_client.submit_order(order)
                print(f"Take Profit detected for {symbol}. Selling {position.qty} shares.")

                # Add symbol and time to frozen symbols
                freeze_symbol(symbol, datetime.now())

            elif short_moving_average > long_moving_average and not position:
                # Golden Cross - Buy Signal
                print('Buy Signal...')

                # Get current buying power
                current_buying_power = float(account.__dict__['buying_power'])
                print(f'Current Buying Power: {current_buying_power}')


                # Check symbol price
                open_price = bars[symbol][-1].open
                
                # Check if we have enough buying power, and buy up to 5 shares
                if open_price < current_buying_power:
                    # Generate order request object
                    # Taking current buying power and dividing by open price to get number of shares
                    quantity = calculate_quantity(current_buying_power, open_price)
                    print(f'Buying {quantity} shares of {symbol} at {open_price}')
                    order = create_buy_order(symbol, quantity)

                    # Submit order
                    trading_client.submit_order(order)
                    print(f"Golden Cross detected for {symbol}. Buying 1 share.")
                
                # If we don't have enough buying power, print a message
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
                print('No Action...')
        else:
            print('Not enough data points...')
        

        # connect to database
        conn = sqlite3.connect('frozen_symbols.db')
        c = conn.cursor()

        # Create table if it doesn't exist
        c.execute('CREATE TABLE IF NOT EXISTS frozen_symbols (symbol TEXT PRIMARY KEY, time TEXT)')

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print('**************************************\n')


if __name__ == '__main__':

     # Get starting portfolio value and time
    account = trading_client.get_account()
    start_portfolio_value = float(account.__dict__['portfolio_value'])
    start_time = datetime.now()

    # Run the main function every 10 minutes until 2:30pm local time
    while True:
        
        # If outside of 8am-2pm local time, exit the program
        if datetime.now().hour < 9 or datetime.now().hour > 14:
            break
        # Otherwise, sleep for 10 minutes
        else:
            # Run main function
            main()
            # Sleep
            print('Sleeping for 10 minutes...')
            sleep(600)
            
    with open('log.txt', 'a') as f:
        # Log ending portfolio value
        account = trading_client.get_account()
        end_portfolio_value = float(account.__dict__['portfolio_value'])

        # Log date and time
        f.write(f'Run started at {start_time} and ended at {datetime.now()}\n')
        
        # Log start and end portfolio values
        f.write(f'Starting Portfolio Value: {start_portfolio_value}\n')
        f.write(f'Ending Portfolio Value: {end_portfolio_value}\n')

        # Log profit, both dollar amount and percentage
        f.write(f'Profit: ${round((end_portfolio_value - start_portfolio_value), 2)}\n')
        f.write(f'Profit Percentage: {round(((end_portfolio_value - start_portfolio_value) / start_portfolio_value), 3)}%\n')
        f.write('**************************************\n')