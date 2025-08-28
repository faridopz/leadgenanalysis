import pandas as pd

# Loading the cleaned leads + conversions dataset
leads_df = pd.read_csv('/Users/faridabdurrahman/Desktop/leadgenanalysis/processed/leads_with_conversion_flag.csv')

# Loading the cleaned interactions dataset
interactions_df = pd.read_csv('/Users/faridabdurrahman/Desktop/leadgenanalysis/processed/cleaned_interactions.csv')

# Merging leads with interactions using lead_id as the common key
# This gives us a row for each interaction, enriched with lead info and conversion flag
full_df = pd.merge(interactions_df, leads_df, on='lead_id', how='left')

# Sort by timestamp so interactions are chronological per lead
full_df = full_df.sort_values(by=['lead_id', 'timestamp'])

# Saving the fully merged dataset
full_df.to_csv('/Users/faridabdurrahman/Desktop/leadgenanalysis/processed/full_merged_dataset.csv', index=False)

# Preview a sample of the final dataset
print(" All datasets merged and saved to 'processed/full_merged_dataset.csv'")
print(full_df.head())
