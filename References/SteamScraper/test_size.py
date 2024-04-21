import pandas as pd

def load_and_check_csv(csv_file):
    # Load CSV file into a DataFrame
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("File not found. Please provide a valid CSV file path.")
        return
    except Exception as e:
        print("An error occurred while loading the CSV file:", str(e))
        return
    
    # Display overview of the data
    print("DataFrame Overview:")
    print("-------------------")
    print("Shape of the DataFrame:", df.shape)
    print("\nData Types:")
    print(df.dtypes)
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nSummary Statistics:")
    print(df.describe())

    print("\n number of app ids: ", len(df["app_id"].unique()))

# Example usage
csv_file_path = "dataset_with_sentiment.csv"  # Change this to your CSV file path
load_and_check_csv(csv_file_path)
