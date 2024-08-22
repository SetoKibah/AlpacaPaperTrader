from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.requests import OrderRequest
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
from time import sleep
from dotenv import load_dotenv
import os
import csv

# Import credentials from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')

# Constants
take_profit = 0.1
profit_stop_loss = 0.05
stop_loss = -0.06
log_file = 'log.csv'
file_exists = os.path.isfile(log_file)

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
           "OMQS", "CLRO", "PRPL", "CODX", "PFIE", "COOK", "SPWH", "SERA", "CLAR", "LFVN", "CRCT",
           "BRDG", "HCAT", "SNFCA", "RXRX", "DOMO", "CLSK", "TRAK", "NATR", "NUS", "MYGN", "VREX", "BYON",
           "PRG", "FC", "ZION", "SKYW", "USNA", "HQY", "MMSI", "UTMD", "IIPR", "EXR"]

# Function to add a symbol to the frozen symbols database
def freeze_symbol(symbol, time):
    try:
        # Connect to database
        conn = sqlite3.connect('frozen_symbols.db')
        c = conn.cursor()

        # Add the frozen symbols to the database
        c.execute('INSERT OR REPLACE INTO frozen_symbols VALUES (?, ?)', (symbol, time.strftime('%Y-%m-%d %H:%M:%S.%f')))

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print(f'Successfully added {symbol} to the frozen symbols database.')
    except Exception as e:
        print(f'Error occurred while adding {symbol} to the frozen symbols database: {str(e)}')

# Function to check if a symbol is frozen
def is_symbol_frozen(symbol):
    try:
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
    except Exception as e:
        print(f'Error occurred while checking if symbol is frozen: {str(e)}')
        return False

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

# Main function
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

# Run main function with additional checks if this file is run directly
if __name__ == '__main__':

     # Get starting portfolio value and time
    account = trading_client.get_account()
    start_portfolio_value = float(account.__dict__['portfolio_value'])
    start_time = datetime.now()

    # Run the main function every 10 minutes until 2:00 pm local time
    while True:
        
        # If outside of 10am-2pm local time, exit the program
        if datetime.now().hour < 10 or datetime.now().hour > 13:
            print('Outside of trading hours, exiting program...')
            break

        # If the day is Saturday or Sunday, exit the program
        if datetime.now().weekday() == 5 or datetime.now().weekday() == 6:
            print('Today is a weekend, exiting program...')
            break

        # List of all holidays nyse is closed in 2024
        holidays = ['2024-01-01', '2024-01-15', '2024-02-19', '2024-03-29', '2024-03-30', '2024-05-27', '2024-07-04', '2024-09-02', '2024-11-28', '2024-12-25']
        # If today is a holiday, exit the program
        if datetime.now().strftime('%Y-%m-%d') in holidays:
            print('Today is a holiday, exiting program...')
            break

        # Otherwise, sleep for 10 minutes
        else:
            # Run main function
            main()
            # Sleep, and show time until next run
            print(f'Sleeping until {datetime.now() + timedelta(minutes=10)}')
            sleep(600)
            
    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)

        # If the file does not exist, write the header
        if not file_exists:
            writer.writerow(['Start Time', 'End Time', 'Starting Portfolio Value', 'Ending Portfolio Value', 'Profit','Profit Percentage'])

        # Log ending portfolio value and time
        account = trading_client.get_account()
        end_portfolio_value = float(account.__dict__['portfolio_value'])
        end_time = datetime.now()

        # Calculate profit and percentage profit
        profit = round((end_portfolio_value - start_portfolio_value), 2)
        profit_percentage = round(((end_portfolio_value - start_portfolio_value) / start_portfolio_value) * 100, 2)

        # Write the log data as new row
        writer.writerow([start_time, end_time, start_portfolio_value, end_portfolio_value, profit, profit_percentage])