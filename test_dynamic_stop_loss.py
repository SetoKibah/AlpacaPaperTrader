from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pandas as pd
from main import calculate_atr, calculate_dynamic_stop_loss

# Import credentials from .env file
print("Loading environment variables...")
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Debug output to verify environment variables
print("API_KEY:", API_KEY if API_KEY else "Not found")
print("API_SECRET:", API_SECRET if API_SECRET else "Not found")

# Initialize clients
client = StockHistoricalDataClient(API_KEY, API_SECRET)
print("StockHistoricalDataClient initialized successfully!")

# Define a list of diverse stocks to test (high volatility, medium, low)
test_symbols = ["TSLA", "AAPL", "MSFT", "T", "PG", "KO", "AMZN", "GME", "VZ"]

# Constants for comparison
FIXED_STOP_LOSS = -0.06  # Original 6% stop loss
ATR_MULTIPLIER = 2.0     # ATR multiplier for dynamic stop loss

# Create a dataframe to store results
results = []

# Test each symbol
for symbol in test_symbols:
    print(f"\nAnalyzing {symbol}...")
    
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)    

    try:
        # Get historical data
        bar_request = StockBarsRequest(
            symbol_or_symbols=symbol, 
            timeframe=TimeFrame(1, TimeFrameUnit('Day')), 
            start=start_date, 
            end=end_date, 
            limit=365)
        
        bars = client.get_stock_bars(bar_request)
        
        if symbol not in bars or len(bars[symbol]) < 20:
            print(f"Not enough data for {symbol}, skipping...")
            continue
            
        # Calculate ATR
        atr = calculate_atr(bars, symbol)
        
        if atr is None:
            print(f"Could not calculate ATR for {symbol}, skipping...")
            continue
        
        # Get current price
        current_price = bars[symbol][-1].close
        last_price = bars[symbol][-2].close  # Previous day's close
        
        # Calculate price volatility (standard deviation of daily returns)
        daily_returns = [(bars[symbol][i].close/bars[symbol][i-1].close - 1) 
                        for i in range(1, len(bars[symbol]))]
        volatility = pd.Series(daily_returns).std() * 100  # Convert to percentage
        
        # Calculate dynamic stop loss based on ATR
        dynamic_stop_loss = calculate_dynamic_stop_loss(current_price, atr, ATR_MULTIPLIER)
        
        # Calculate ATR as percentage of price
        atr_percentage = (atr / current_price) * 100
        
        # Calculate daily price change
        daily_change = (current_price / last_price - 1) * 100
        
        # Store results
        results.append({
            'Symbol': symbol,
            'Price': current_price,
            'ATR': atr,
            'ATR %': atr_percentage,
            'Fixed Stop Loss %': FIXED_STOP_LOSS * 100,
            'Dynamic Stop Loss %': dynamic_stop_loss * 100,
            'Volatility %': volatility,
            'Daily Change %': daily_change
        })
        
        print(f"Price: ${current_price:.2f}")
        print(f"ATR: ${atr:.4f} ({atr_percentage:.2f}%)")
        print(f"Fixed Stop Loss: {FIXED_STOP_LOSS*100:.2f}%")
        print(f"Dynamic Stop Loss: {dynamic_stop_loss*100:.2f}%")
        print(f"30-Day Volatility: {volatility:.2f}%")
        print(f"Daily Change: {daily_change:.2f}%")
        
    except Exception as e:
        print(f"Error processing {symbol}: {str(e)}")

# Convert results to dataframe for better display
if results:
    df = pd.DataFrame(results)
    print("\n--- COMPARISON RESULTS ---")
    print(df.sort_values(by='Volatility %', ascending=False))
    
    # Save results to CSV
    df.to_csv('stop_loss_comparison.csv', index=False)
    print("Results saved to stop_loss_comparison.csv")
else:
    print("No results generated. Check for errors above.")
