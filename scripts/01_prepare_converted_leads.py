import pandas as pd

# Load leads and conversions data
leads_df = pd.read_csv('/Users/faridabdurrahman/Desktop/leadgenanalysis/data/leads.csv')
conversions_df = pd.read_csv('/Users/faridabdurrahman/Desktop/leadgenanalysis/data/conversions.csv')

# Add a 'converted' flag to leads_df
leads_df['converted'] = leads_df['lead_id'].isin(conversions_df['lead_id']).astype(int)

# Save the updated leads file with conversion flag
leads_df.to_csv('/Users/faridabdurrahman/Desktop/leadgenanalysis/processed/leads_with_conversion_flag.csv', index=False)

# Print confirmation
conversion_counts = leads_df['converted'].value_counts().rename_axis('converted').reset_index(name='count')
print(" leads_with_conversion_flag.csv created.")
print("Conversion Breakdown:\n", conversion_counts)
