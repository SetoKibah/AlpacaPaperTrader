# Alpaca Paper Trader

## Project Overview
This project is a trading application that integrates with Alpaca's API to perform sentiment analysis, backtesting, and strategy evaluation for stock trading.

## Features
- Sentiment analysis of news articles using NLTK's VADER.
- Backtesting trading strategies.
- Performance evaluation of trading strategies.
- Database management for stock tickers and logs.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```env
     APCA_API_KEY_ID=your_api_key_id
     APCA_API_SECRET_KEY=your_api_secret_key
     ```

4. Run the application:
   ```bash
   python main.py
   ```

## Testing
Run unit tests using:
```bash
pytest
```

## Contribution Guidelines
- Fork the repository and create a new branch for your feature or bug fix.
- Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License.
