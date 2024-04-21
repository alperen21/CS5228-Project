import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import time
import numpy as np

existing_df_file = "dataset.csv"
file_to_save = "app_list_existing.csv"


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
    print("Start extracting app_ids...\n")

    df_old = pd.read_csv(existing_df_file)
    appids = read_appids_from_df(df_old)
    np.savetxt(file_to_save, appids, delimiter=",")
    



if __name__ == "__main__":
    main()
