from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.trading.client import TradingClient

API_KEY = 'PKYM44C7PI5RTRX7LFSG'
API_SECRET = 'cXy7euUOQ1jfXQN8kWUthG4EIHN3uv8CzCPaqngT'
BASE_URL = 'https://paper-api.alpaca.markets'  # use this for paper trading

client = StockHistoricalDataClient(API_KEY,API_SECRET)
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)

multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=["F", "GE", "NOK"])

latest_multisymbol_quotes = client.get_stock_latest_quote(multisymbol_request_params)

#for item in latest_multisymbol_quotes["NOK"]:
#    print(item)

#print(latest_multisymbol_quotes["NOK"].ask_price)

account = trading_client.get_account()
for property_name, value in account:
    print(f"\"{property_name}\": {value}")