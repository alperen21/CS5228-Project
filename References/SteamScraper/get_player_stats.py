import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import time
import math

# Your Steam API key
API_KEY = 'F07D7ED5C43A695B3EBB01C28B6A18E5'
header = {"Client-ID": API_KEY}
# list of app ids
applist_filename = "app_list_new.txt"

def read_appids_from_list(filename):
    appids = []
    with open(filename) as file:
        for line in file:
            appids.append(int(line.strip()))
    return appids

def get_current_player_count(app_id):
    game_players_url = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid=' + str(app_id)
    game_players = requests.get(game_players_url, headers=header).json()['response']['player_count']
    print(f"current players: {game_players} for id {app_id}")

    return game_players

def get_review_summary(app_id):
    # Steam Web API URL for GetReviewsSummary endpoint
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
    summary_info = []

    try:
        # Sending GET request to the Steam Web API
        response = requests.get(url)
        data = response.json()

        # Check if request was successful
        if response.status_code == 200:
            # Extracting total number of reviews from response
            total_reviews = data['query_summary']['total_reviews']
            total_positive = data['query_summary']['total_positive']
            total_negative = data['query_summary']['total_negative']
            summary_info = [total_reviews, total_positive, total_negative]

            # # save json for viewing
            # with open("test_check_review_summary.json", 'w') as f:
            #     json.dump(data, f)
            return summary_info
        else:
            # If request was unsuccessful, print error message
            print(f"Error: {data['error']}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_review_stats(appid):
    df_headers = ['app_id', 'current_players', 'total_reviews', 'total_positive', 'total_negative', 'score', 'rating']
    stats = []
    count = get_current_player_count(appid)
    summary = get_review_summary(appid)
    if summary[0] == 0: 
        score = 0.5
    else:
        score = summary[1] / summary[0]
    rating = score - (score - 0.5) * math.pow(2, 0-math.log(summary[0] + 1, 10))
    stats.append([appid, count, summary[0], summary[1], summary[2], score, rating])
    df = pd.DataFrame(stats, columns=df_headers)
    return df

def main():
    summaries = []
    appids = read_appids_from_list(applist_filename)
    for appid in appids:
        df = get_review_stats(appid)
        summaries.append(df)
    combined = pd.concat(summaries)
    combined.to_csv("test_stats_data.csv")

    print("complete getting app summaries in main()")


if __name__ == "__main__":
    main()
