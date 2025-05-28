from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
import os

# Load environment variables
print("Loading environment variables...")
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')

# Display API credentials (partially masked for security)
if API_KEY:
    masked_key = API_KEY[:4] + "..." + API_KEY[-4:] if len(API_KEY) > 8 else "Invalid key format"
    print(f"API_KEY: {masked_key}")
else:
    print("API_KEY: Not found")
    
if API_SECRET:
    masked_secret = API_SECRET[:4] + "..." + API_SECRET[-4:] if len(API_SECRET) > 8 else "Invalid secret format"
    print(f"API_SECRET: {masked_secret}")
else:
    print("API_SECRET: Not found")
    
print(f"BASE_URL: {BASE_URL}")

# Test Alpaca connections
print("\n=== Testing Alpaca Connections ===")

try:
    print("\nTesting StockHistoricalDataClient connection...")
    data_client = StockHistoricalDataClient(API_KEY, API_SECRET)
    print("✓ StockHistoricalDataClient connection successful!")
except Exception as e:
    print(f"✗ StockHistoricalDataClient connection failed: {e}")

try:
    print("\nTesting TradingClient connection...")
    trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
    account = trading_client.get_account()
    print("✓ TradingClient connection successful!")
    print(f"Account Status: {account.status}")
    print(f"Account Buying Power: ${account.buying_power}")
    print(f"Account Portfolio Value: ${account.portfolio_value}")
except Exception as e:
    print(f"✗ TradingClient connection failed: {e}")

print("\nConnection test complete!")