import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import time


applist_filename = "app_list_new.txt"

def get_reviews(appid, params={"json": 1}):
    url = "https://store.steampowered.com/appreviews/"
    response = requests.get(
        url=url + appid, params=params, headers={"User-Agent": "Mozilla/5.0"}
    ).json()
    return response


def get_n_reviews(appid, n=100):
    reviews = []
    cursor = "*"
    params = {
        "json": 1,
        "filter": "all",
        "language": "english",
        "day_range": 9223372036854775807,
        "review_type": "all",
        "purchase_type": "all",
    }

    while n > 0:
        params["cursor"] = cursor.encode()
        params["num_per_page"] = min(100, n)
        n -= 100

        response = get_reviews(appid, params)
        cursor = response["cursor"]
        reviews += response["reviews"]

        if len(response["reviews"]) < 100:
            break

    return reviews


def get_app_id(game_name):
    response = requests.get(
        url=f"https://store.steampowered.com/search/?term={game_name}&category1=998",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    soup = BeautifulSoup(response.text, "html.parser")
    app_id = soup.find(class_="search_result_row")["data-ds-appid"]
    return app_id


def get_n_appids(n=100, filter_by="topsellers"):
    appids = []
    url = (
        f"https://store.steampowered.com/search/?category1=998&filter={filter_by}&page="
    )
    page = 0

    while page * 25 < n:
        page += 1
        response = requests.get(
            url=url + str(page), headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(response.text, "html.parser")
        for row in soup.find_all(class_="search_result_row"):
            appids.append(row["data-ds-appid"])

    return appids[:n]

def read_appids_from_list(filename):
    appids = []
    with open(filename) as file:
        for line in file:
            appids.append(appids.append(int(line.strip())))

    return appids


def main():
    # appid_num_to_get = 5
    review_num_to_get = 1000
    reviews = []
    

    start_time = time.time()
    print("Start collection...\n")
    # appids = get_n_appids(appid_num_to_get)
    appids = read_appids_from_list(applist_filename)
    appid_num_to_get = len(appids)
    for appid in appids:
        reviews_one_game = get_n_reviews(appid, review_num_to_get)
        df = pd.DataFrame(reviews_one_game)
        df["app_id"] = appid
        reviews.append(df)
        time.sleep(5)

    combined = pd.concat(reviews)
    combined.to_csv(f"steam_{appid_num_to_get}_ids_{review_num_to_get}_reviews.csv")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Time elapsed:", elapsed_time, "seconds\n")
    print(
        f"scraping {appid_num_to_get} ids with {review_num_to_get} reviews each complete!\n"
    )


if __name__ == "__main__":
    main()
