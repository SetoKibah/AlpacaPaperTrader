import mibian
import yfinance as yf

# Download historical market data
pltr = yf.Ticker("PLTR")
pltr_history = pltr.history(period="1d")

# Get the last closing price
underlying_price = pltr_history['Close'][-1]

# Define the strike price and the risk-free rate
strike_price = 100
risk_free_rate = 1  # 1% risk-free rate

# Define the market call and put prices
market_call_price = 10
market_put_price = 10

# Calculate the implied volatility for call
c = mibian.BS([underlying_price, strike_price, risk_free_rate, 30], callPrice=market_call_price)
print("Call implied volatility: ", c.impliedVolatility)

# Calculate the implied volatility for put
p = mibian.BS([underlying_price, strike_price, risk_free_rate, 30], putPrice=market_put_price)
print("Put implied volatility: ", p.impliedVolatility)

# Decide whether to do a call or a put
if c.impliedVolatility > p.impliedVolatility:
    print("Do a call")
elif c.impliedVolatility < p.impliedVolatility:
    print("Do a put")
else:
    print("Both call and put have the same implied volatility")