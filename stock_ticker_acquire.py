# Description: This script gets all the NASDAQ symbols and saves them as a CSV file.

# Import libraries
import pandas as pd
from pandas_datareader import data as pdr
from tqdm import tqdm
from time import sleep

print("Starting script...")

# Get NASDAQ symbols
print("Getting NASDAQ symbols...")
url_nasdaq = 'http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt'
df_nasdaq = pd.read_csv(url_nasdaq, sep='|')

nasdaq_symbols = [symbol for symbol in tqdm(df_nasdaq[df_nasdaq['Test Issue'] == 'N']['NASDAQ Symbol'].tolist(), desc="Getting NASDAQ symbols")]

# Print length of the list
print(f"Number of tickers: {len(nasdaq_symbols)}")

# Save the list as a CSV file
print("Saving the list as a CSV file...")
df = pd.DataFrame(nasdaq_symbols, columns=["Ticker"])
df.to_csv('tickers.csv', index=False)

print("Program finished.")
