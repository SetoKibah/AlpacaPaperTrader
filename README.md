# Stock Trading Bot

This project is a stock trading bot that interacts with the Alpaca API to automate stock trading based on predefined strategies. The bot is designed to run continuously, checking for trading opportunities and logging its activities.

## Project Structure

```
__pycache__/
.gitignore
backtest.py
evaluate_performance.py
log.txt
main.py
nasdaq_raw.csv
requirements.txt
stock_ticker_acquire.py
test_option_strategy.py
test.py
ticker_assessment.py
tickers.csv
unit_tests.py
view_database.py
```

### Key Files

- **main.py**: The main script that runs the trading bot. It initializes the Alpaca API clients, manages the trading loop, and logs trading activities.
- **ticker_assessment.py**: Contains functions to assess stock tickers and determine trading opportunities.
- **backtest.py**: Used for backtesting trading strategies.
- **evaluate_performance.py**: Evaluates the performance of the trading strategies.
- **stock_ticker_acquire.py**: Acquires stock ticker data.
- **view_database.py**: Views and manages the database of frozen symbols.
- **unit_tests.py**: Contains unit tests for the project.

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the root directory and add your Alpaca API credentials:
    ```
    API_KEY=your_api_key
    API_SECRET=your_api_secret
    BASE_URL=https://paper-api.alpaca.markets
    ```

4. **Prepare the database**:
    The bot uses an SQLite database to manage frozen symbols. The database will be created automatically if it doesn't exist.

## Usage

Run the main script to start the trading bot:
```sh
python main.py
```

### Main Script ([`main.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Ff%3A%2FPersonal%20Programming%20Projects%2FTrading%2FAlpacaPaperTrader%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "f:\Personal Programming Projects\Trading\AlpacaPaperTrader\main.py"))

- **Initialization**:
    - Loads API credentials from the `.env` file.
    - Initializes Alpaca API clients.
    - Connects to the SQLite database and creates the `frozen_symbols` table if it doesn't exist.

- **Trading Loop**:
    - Checks if today is a holiday. If it is, the bot exits.
    - Runs the [`main`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Ff%3A%2FPersonal%20Programming%20Projects%2FTrading%2FAlpacaPaperTrader%2Fmain.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A117%2C%22character%22%3A4%7D%5D "main.py") function to perform trading operations.
    - Sleeps for 10 minutes before the next iteration.

- **Logging**:
    - Logs trading activities to `log.csv`.
    - Records the start and end portfolio values, profit, and profit percentage.

### Ticker Assessment ([`ticker_assessment.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Ff%3A%2FPersonal%20Programming%20Projects%2FTrading%2FAlpacaPaperTrader%2Fticker_assessment.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "f:\Personal Programming Projects\Trading\AlpacaPaperTrader\ticker_assessment.py"))

- **Initialization**:
    - Loads API credentials and initializes Alpaca API clients.
    - Loads stock tickers from [`tickers.csv`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Ff%3A%2FPersonal%20Programming%20Projects%2FTrading%2FAlpacaPaperTrader%2Ftickers.csv%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "f:\Personal Programming Projects\Trading\AlpacaPaperTrader\tickers.csv").

- **Ticker Analysis**:
    - Iterates over the tickers and retrieves historical stock data.
    - Calculates trends and determines trading opportunities.

## Functions

### [`main.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Ff%3A%2FPersonal%20Programming%20Projects%2FTrading%2FAlpacaPaperTrader%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "f:\Personal Programming Projects\Trading\AlpacaPaperTrader\main.py")

- **`freeze_symbol(symbol, time)`**: Adds a symbol to the frozen symbols database.
- **[`is_symbol_frozen(symbol)`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Ff%3A%2FPersonal%20Programming%20Projects%2FTrading%2FAlpacaPaperTrader%2Fmain.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A63%2C%22character%22%3A4%7D%5D "main.py")**: Checks if a symbol is frozen.
- **`moving_average(lst, window_size)`**: Calculates the moving average.
- **`calculate_quantity(current_buying_power, open_price)`**: Calculates the quantity of shares to buy.
- **`create_buy_order(symbol, quantity)`**: Creates a buy order request.
- **[`main()`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Ff%3A%2FPersonal%20Programming%20Projects%2FTrading%2FAlpacaPaperTrader%2Fmain.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A117%2C%22character%22%3A4%7D%5D "main.py")**: The main function that performs trading operations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

This README provides an overview of the project and instructions on how to set it up and run it. For more detailed information, please refer to the individual scripts and their respective comments and documentation.
