import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import ssl

csv_file_path = "steam_1000_ids_tokenized_summary_reviews.csv"

def update_nltk():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download('punkt')
    nltk.download('vader_lexicon')

# Function to calculate sentiment scores
def calculate_sentiment_score(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    return scores['compound']

# Load the dataset
def add_sentiment_column(csv_file):
    try:
        # Load the dataset
        df = pd.read_csv(csv_file)
        column_to_drop = 'Unnamed: 0.1'  
        if column_to_drop in df.columns:
            df.drop(columns=column_to_drop, inplace=True)
        column_to_drop = 'Unnamed: 0' 
        if column_to_drop in df.columns:
            df.drop(columns=column_to_drop, inplace=True)
        df["review_text"] = df["review_text"].astype(str)
    except FileNotFoundError:
        print("File not found. Please provide a valid CSV file path.")
        return

    # Add a new column 'sentiment_score' based on the 'review_text' column
    df['sentiment_score'] = df['review_text'].apply(calculate_sentiment_score)

    return df

update_nltk()
# Example usage
df_with_sentiment = add_sentiment_column(csv_file_path)

# Save the DataFrame with the added sentiment column to a new CSV file
if df_with_sentiment is not None:
    df_with_sentiment.to_csv("dataset_with_sentiment.csv", index=False)
    print("DataFrame with sentiment score saved to 'dataset_with_sentiment.csv'.")
