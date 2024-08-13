import backtrader as bt
import yfinance as yf

class VolatilityStrategy(bt.Strategy):
    params = (
        ("atr_period", 14),
        ("rsi_period", 14),
        ("rsi_overbought", 70),
        ("rsi_oversold", 30),
        ("stop_loss", 0.02),  # 2% stop-loss
        ("take_profit", 0.04),  # 4% take-profit
    )

    def __init__(self):
        self.atr = bt.indicators.ATR(self.data.close, period=self.params.atr_period)
        self.rsi = bt.indicators.RelativeStrengthIndex(period=self.params.rsi_period)

    def next(self):
        if self.rsi < self.params.rsi_oversold and self.data.close > self.data.close[0] + self.atr[0] * self.params.stop_loss:
            # Buy signal with RSI oversold condition and dynamic stop-loss
            self.buy()
        elif self.rsi > self.params.rsi_overbought or self.data.close > self.data.close[0] + self.atr[0] * self.params.take_profit:
            # Sell signal or take-profit
            self.sell()

# Download historical data using yfinance
data = yf.download('AAPL', start='2022-01-01', end='2023-12-06')

# Create a cerebro engine
cerebro = bt.Cerebro()

# Add a data feed
cerebro.adddata(bt.feeds.PandasData(dataname=data))

# Add the volatility strategy
cerebro.addstrategy(VolatilityStrategy)

# Set initial cash
cerebro.broker.set_cash(1000)  # Use 1000 for your initial account value

# Set commission - 0.1% ... divide by 100 to remove the %
cerebro.broker.setcommission(commission=0.001)

# Print the starting cash
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run the strategy
cerebro.run()

# Print the final cash
print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Plot the results
cerebro.plot(style='candlestick')
