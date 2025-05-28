import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Print the environment variables to verify they are loaded
print("API_KEY:", os.getenv("API_KEY"))
print("API_SECRET:", os.getenv("API_SECRET"))
print("BASE_URL:", os.getenv("BASE_URL"))
