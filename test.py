import requests
import json

url = "https://data.alpaca.markets/v2/stocks/bars/latest?symbols=F&feed=iex"

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": "PKSOVG2YEBLVPKNA8K5U",
    "APCA-API-SECRET-KEY": "09rRznBcGib14PmuAet5ctzhjA6F9vZzCjqEQC71"
}

response = requests.get(url, headers=headers)

data = response.json()

print(data['bars']['F'].keys())
for key, item in data['bars']['F'].items():
    print(f'{key}: {item}')
