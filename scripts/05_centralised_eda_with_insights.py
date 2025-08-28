# scripts/04_centralised_eda_with_insights.py
import pandas as pd

# Load merged dataset
df = pd.read_csv('/Users/faridabdurrahman/Desktop/leadgenanalysis/processed/full_merged_dataset.csv')

# Ensure date parsing
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
if 'conversion_date' in df.columns:
    df['conversion_date'] = pd.to_datetime(df['conversion_date'], errors='coerce')

print("\nRunning Centralised EDA...")

# 1. Channel & Quality Interaction
channel_quality = df.groupby('source_channel').agg(
    avg_quality_score=('lead_quality_score', 'mean'),
    conversion_rate=('converted', 'mean'),
    total_leads=('lead_id', 'count'),
    converted_leads=('converted', 'sum')
).reset_index()

print("\nChannel & Quality Interaction:")
best_channel = channel_quality.sort_values(by='conversion_rate', ascending=False).iloc[0]
print(f"- Highest converting channel: {best_channel['source_channel']} "
      f"({best_channel['conversion_rate']:.2%} conversion rate, Avg Quality Score: {best_channel['avg_quality_score']:.2f})")

# 2. Campaign Performance
campaign_perf = df.groupby('campaign_id').agg(
    total_leads=('lead_id', 'count'),
    converted_leads=('converted', 'sum'),
    conversion_rate=('converted', 'mean'),
    avg_quality_score=('lead_quality_score', 'mean')
).reset_index().sort_values(by='conversion_rate', ascending=False)

top_campaign = campaign_perf.iloc[0]
print("\nCampaign Performance:")
print(f"- Best campaign by conversion rate: {top_campaign['campaign_id']} "
      f"({top_campaign['conversion_rate']:.2%}, {top_campaign['total_leads']} leads)")

# 3. Conversion Timing
if 'conversion_date' in df.columns:
    df['days_to_convert'] = (df['conversion_date'] - df['created_at']).dt.days
    conversion_timing = df[df['converted'] == 1][['lead_id', 'days_to_convert', 'source_channel', 'campaign_id']]
    avg_days = conversion_timing['days_to_convert'].mean()
    print("\nConversion Timing:")
    print(f"- Average time to convert: {avg_days:.1f} days")
else:
    conversion_timing = pd.DataFrame(columns=['lead_id', 'days_to_convert', 'source_channel', 'campaign_id'])
    print("\nConversion Timing: No conversion date data available.")

# 4. Device Preference by Channel
device_pref = df.groupby(['source_channel', 'device_type']).agg(
    converted_leads=('converted', 'sum'),
    conversion_rate=('converted', 'mean')
).reset_index()

best_device = device_pref.sort_values(by='conversion_rate', ascending=False).iloc[0]
print("\nDevice Preference by Channel:")
print(f"- Best performing device/channel combo: {best_device['device_type']} via {best_device['source_channel']} "
      f"({best_device['conversion_rate']:.2%} conversion rate)")

# 5. Repeat Interactions
if 'interaction_id' in df.columns:
    interactions_per_lead = df.groupby(['lead_id', 'converted'])['interaction_id'].count().reset_index(name='num_interactions')
    repeat_interactions = interactions_per_lead.groupby('converted').agg(
        avg_interactions=('num_interactions', 'mean'),
        median_interactions=('num_interactions', 'median'),
        max_interactions=('num_interactions', 'max')
    ).reset_index()

    converted_avg = repeat_interactions[repeat_interactions['converted'] == 1]['avg_interactions'].values[0]
    nonconverted_avg = repeat_interactions[repeat_interactions['converted'] == 0]['avg_interactions'].values[0]

    print("\nRepeat Interactions:")
    print(f"- Converted leads average {converted_avg:.1f} interactions vs {nonconverted_avg:.1f} for non-converted leads")
else:
    repeat_interactions = pd.DataFrame(columns=['converted', 'avg_interactions', 'median_interactions', 'max_interactions'])
    print("\nRepeat Interactions: No interaction data available.")

# Save to Excel
output_path = '/Users/faridabdurrahman/Desktop/leadgenanalysis/processed/lead_analysis_summary.xlsx'
with pd.ExcelWriter(output_path) as writer:
    channel_quality.to_excel(writer, sheet_name='Channel_Quality', index=False)
    campaign_perf.to_excel(writer, sheet_name='Campaign_Performance', index=False)
    conversion_timing.to_excel(writer, sheet_name='Conversion_Timing', index=False)
    device_pref.to_excel(writer, sheet_name='Device_Pref_by_Channel', index=False)
    repeat_interactions.to_excel(writer, sheet_name='Repeat_Interactions', index=False)

print(f"\nAnalysis complete. Saved to: {output_path}")
