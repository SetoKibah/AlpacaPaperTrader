import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Debugging: Print environment variables to verify they are loaded correctly
print("API_KEY:", os.getenv("API_KEY"))
print("API_SECRET:", os.getenv("API_SECRET"))

# Example URL for the News API
url = "https://data.alpaca.markets/v1beta1/news?start=2024-06-04T00%3A00%3A00Z&end=2024-08-26T00%3A00%3A00Z&sort=desc&symbols=F&include_content=true&exclude_contentless=true"

def calculate_average_sentiment(url):
    # Download the VADER lexicon if not already downloaded
    nltk.download('vader_lexicon')

    # Retrieve API keys from environment variables
    api_key_id = os.getenv("API_KEY")
    api_secret_key = os.getenv("API_SECRET")

    if not api_key_id or not api_secret_key:
        raise ValueError("API keys are not set in the environment variables.")

    # Set up the API request headers
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key_id,
        "APCA-API-SECRET-KEY": api_secret_key
    }

    try:
        # Send the API request and get the response
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        news_list = response.json().get('news', [])

        if not news_list:
            raise ValueError("No news data found in the API response.")

        # Initialize the sentiment scores list
        sentiment_scores = []

        # Create a SentimentIntensityAnalyzer object
        sia = SentimentIntensityAnalyzer()

        # Iterate over the news articles and calculate sentiment scores
        for news in news_list:
            test_sentiment = news.get('summary', '')
            if test_sentiment:
                sentiment = sia.polarity_scores(test_sentiment)
                sentiment_scores.append(sentiment['compound'])

        if not sentiment_scores:
            raise ValueError("No sentiment scores could be calculated.")

        # Calculate the average sentiment score
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)

        return average_sentiment

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"An error occurred while making the API request: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")

