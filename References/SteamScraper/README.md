# How to use
## `test_scraper.py` -- a basic script to test functionality
1. Replace the `app_id` with the id of the target game on Steam
2. Run `python3 test_scraper.py`
3. The json data of the reviews will be saved as `data.json` in the project directory

## `steam_scrape_full.py` -- the final script to pull customized size of reviews
1. Replace the `appid_num_to_get` with the number of top rated games on steam for data collection.
2. Replace the `review_num_to_get` with the number of reviews to collect for each game
3. The output `.csv` file will be `steam_x_ids_y_reviews.csv`

# Reference
Based on blog of [Medium: Scraping Steam User Reviews](https://andrew-muller.medium.com/scraping-steam-user-reviews-9a43f9e38c92)