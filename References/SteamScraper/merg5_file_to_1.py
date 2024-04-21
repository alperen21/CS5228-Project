import pandas as pd

def merge_csv_files(csv_files):
    # List to store DataFrames
    dfs = []

    # Load each CSV file into a DataFrame
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
        except FileNotFoundError:
            print(f"File '{file}' not found. Skipping...")

    # Check if any DataFrames were loaded
    if not dfs:
        print("No valid CSV files found.")
        return None

    # Merge DataFrames
    merged_df = dfs[0]  # Start with the first DataFrame
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, how='outer')

    return merged_df

# Example usage
csv_files = ["online_200_ids_summary.csv", "online_201_ids_summary_200_to_400.csv", "online_201_ids_summary_400_to_600.csv", "online_201_ids_summary_600_to_800.csv", "online_201_ids_summary_800_to_1000.csv"]  # Replace with your CSV file paths
# merged_dataframe = merge_csv_files(csv_files).drop_duplicates(subset=["app_id"], keep="first",inplace=True)
merged_dataframe = merge_csv_files(csv_files)
merged_dataframe.drop_duplicates(subset=["app_id"], keep="first")


print(f"now you have {merged_dataframe.shape[0]} app ids")

# Save the merged DataFrame to a new CSV file
if merged_dataframe is not None:
    merged_dataframe.to_csv("online_1000_ids_summary.csv", index=False)
    print("Merged DataFrame saved to 'online_1000_ids_summary.csv'.")
