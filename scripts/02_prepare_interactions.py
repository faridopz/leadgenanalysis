import pandas as pd

# Loading the raw interactions data from the data folder
interactions_df = pd.read_csv('/Users/faridabdurrahman/Desktop/leadgenanalysis/data/interactions.csv')

# Converting the timestamp column to proper datetime format to work with it easily later
interactions_df['timestamp'] = pd.to_datetime(interactions_df['timestamp'], errors='coerce')

# Removing rows that are missing either lead_id or timestamp since they’re not useful for analysis
interactions_df = interactions_df.dropna(subset=['lead_id', 'timestamp'])

# Cleaning up text fields by converting them to lowercase and stripping any extra spaces
interactions_df['interaction_type'] = interactions_df['interaction_type'].str.lower().str.strip()
interactions_df['channel'] = interactions_df['channel'].str.lower().str.strip()
interactions_df['device_type'] = interactions_df['device_type'].str.lower().str.strip()

# Saving the cleaned interactions data to the processed folder for later use
interactions_df.to_csv('/Users/faridabdurrahman/Desktop/leadgenanalysis/processed/cleaned_interactions.csv', index=False)

# Displaying a sample of the cleaned data just to quickly confirm it worked
print(" Interactions cleaned and saved to 'processed/cleaned_interactions.csv'")
print(interactions_df.head())
