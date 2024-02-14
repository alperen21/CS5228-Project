import requests
import json

app_id = "1623730"
scraped_data_name = 'steam_reviews_scraped.json'
response = requests.get(url=f'https://store.steampowered.com/appreviews/{app_id}?json=1').json()
# print(response)

with open(scraped_data_name, 'w') as f:
    json.dump(response, f)