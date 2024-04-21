import pandas as pd
import nltk
import re
import ssl

public_file_path = 'steam_6_ids_1000_summary_reviews_hotGames.csv'
# nltk.download('punkt')

def update_nltk():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download('punkt')

def get_df_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    # Regular expression to match non-verbal text such as emojis or symbols
    nonverbal_pattern = re.compile(r'[\W_]+')
    # Filter out non-verbal tokens
    filtered_tokens = [token for token in tokens if not nonverbal_pattern.match(token)]
    
    return filtered_tokens

def tokenize_all_text(df_target, target_col = "review"):
    df_target[target_col] = df_target[target_col].astype(str)
    df_target[target_col].dropna(inplace=True)
    df_target["review_tokenised"] = df_target[target_col].copy()
    df_target["review_tokenised"] = df_target["review_tokenised"].apply(lambda text: tokenize_text(text))
    return df_target

def main():
    update_nltk()
    df_old = get_df_from_csv(public_file_path)
    df_updated = tokenize_all_text(df_old)
    df_updated.to_csv(public_file_path.replace(".csv", "_tokenized.csv"))


if __name__ == "__main__":
    main()

