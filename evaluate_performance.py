from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
import os
import time
from dotenv import load_dotenv

# Assume a starting portfolio of $1,000
portfolio = 1000


# Import credentials from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')

# Initialize the Alpaca API client
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)

# Generate order request for closed positions starting November 1, 2023 and ending February 20, 2024
order_request = GetOrdersRequest(
    start_time="2023-11-01T00:00:00Z",
    end_time="2024-02-20T00:00:00Z",
    status="closed"
)

# Get the order history
order_history = trading_client.get_orders(order_request)
# https://github.com/alpacahq/alpaca-py/blob/master/alpaca/trading/models.py

# Checking against the portfolio, calculate the performance of the portfolio from the order history
# For each order, calculate the total value of the order, and add it to the portfolio
# If the order is a buy, subtract the total value from the portfolio
# If the order is a sell, add the total value to the portfolio
# Print the performance of the portfolio
for order in order_history:
    if order.canceled_at is None:
        if order.side == 'buy':
            portfolio -= int(order.filled_qty) * float(order.filled_avg_price)
        else:
            portfolio += int(order.filled_qty) * float(order.filled_avg_price)
    else:
        continue
print(f"Portfolio Performance: ${portfolio}")
print(f"Number of orders: {len(order_history)}")











#for order in order_history:
#    print(f"Symbol: {order.symbol}, Side: {order.side}, Qty: {order.qty}, Price: {order.filled_avg_price}, Time: {order.filled_at}")
#    print('**************************************')
#    time.sleep(30)

