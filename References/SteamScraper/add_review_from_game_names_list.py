import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import time
import get_player_stats
import tokenize_review_in_csv


applist_filename = "app_list_hot.txt"
# existing_df_file = "sentiment_1000_dataset.csv"
# existing_df_file = "steam_5_ids_1000_reviews.csv"
existing_df_file = "dataset.csv"
num_appids_to_collect = 10

def get_reviews(appid, params={"json": 1}):
    url = "https://store.steampowered.com/appreviews/"
    response = requests.get(
        url=url + str(appid), params=params, headers={"User-Agent": "Mozilla/5.0"}
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
        try:
            cursor = response["cursor"]
            reviews += response["reviews"]

            if len(response["reviews"]) < 100:
                break
        except:
            reviews += response["reviews"]
            return reviews

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
            appids.append(int(line.strip()))

    return appids

def read_appids_from_df(df_old):
    appids = df_old["app_id"].unique()
    return appids

def get_first_n_appids_df(df_old, app_num):
    top_n_appids = df_old["app_id"].value_counts().head(app_num).index.tolist()
    filtered_df = df_old[df_old["app_id"].isin(top_n_appids)]
    return filtered_df


def main():
    summaries = []

    start_time = time.time()
    print("Start collection...\n")

    df_all = pd.read_csv(existing_df_file)
    df_old = get_first_n_appids_df(df_all, num_appids_to_collect)
    # appids = read_appids_from_df(df_old)
    appids = read_appids_from_df(df_old)
    appid_num_to_get = len(appids)
    count = 0
    for appid in appids:
        # print(f"loading appid: {appid} ...")
        df_stats = get_player_stats.get_review_stats(appid)
        summaries.append(df_stats)
        count += 1

        if count >= 300:
            count = 0
            time.sleep(100)

    df_all_summaries = pd.concat(summaries)
    df_merged = pd.merge(df_old, df_all_summaries, on='app_id', how="inner")

    df_merged.to_csv(f"preivew_{appid_num_to_get}_ids_summary.csv")

    df_tokenized = tokenize_review_in_csv.tokenize_all_text(df_merged, "review_text")

    df_tokenized.to_csv(f"steam_{appid_num_to_get}_ids_tokenized_summary_reviews.csv")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Time elapsed:", elapsed_time, "seconds\n")
    print(
        f"editing {existing_df_file} ids with reviews summary is complete!\n"
    )


if __name__ == "__main__":
    main()
