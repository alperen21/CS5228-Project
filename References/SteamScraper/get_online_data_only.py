import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import time
import get_player_stats
import tokenize_review_in_csv
import numpy as np

# existing_df_file = "dataset.csv"
app_list_file = "app_list_existing.csv"
starting_index = 800
num_appids_to_collect = 200


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

    app_ids_all = np.genfromtxt(app_list_file, delimiter=",")
    print(f"get {len(app_ids_all)} ids from {app_list_file}")
    print(f"get first {num_appids_to_collect} ids and online data")
    appids = app_ids_all[starting_index:starting_index + num_appids_to_collect + 1]
    appid_num_to_get = len(appids)
    count = 0
    for appid in appids:
        # print(f"loading appid: {appid} ...")
        df_stats = get_player_stats.get_review_stats(appid)
        summaries.append(df_stats)
        count += 1

        if count >= 100:
            count = 0
            print(f"----- reach 100 counts, sleep for 20 -----")
            time.sleep(20)

    df_all_summaries = pd.concat(summaries)

    df_all_summaries.to_csv(f"online_{appid_num_to_get}_ids_summary_{starting_index}_to_{starting_index + num_appids_to_collect}.csv")


    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Time elapsed:", elapsed_time, "seconds\n")
    print(
        f"collecting {num_appids_to_collect} ids with reviews summary is complete!\n"
    )


if __name__ == "__main__":
    main()
