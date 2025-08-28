# master_regeneration_eda.py
# Author: Farid Abdurrahman
# Purpose: Clean, analyse, and regenerate insights for my lead generation dataset.
# Why: I wanted an organised way to explore lead behaviour, sources, and quality — 
#      so I can quickly identify patterns that could guide future campaigns.

import pandas as pd
import os

# ====== 1. SETUP ======
# Define dataset path — pointing directly to my processed folder
data_path = "/Users/faridabdurrahman/desktop/leadgenanalysis/processed/full_merged_dataset.csv"

# Define where processed outputs will go
output_dir = "/Users/faridabdurrahman/desktop/leadgenanalysis/processed"
os.makedirs(output_dir, exist_ok=True)

# ====== 2. LOAD DATA ======
try:
    df = pd.read_csv(data_path)
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print(f"ERROR: File not found at {data_path}")
    exit()

# Quick look
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}\n")

# ====== 3. BASIC CLEANING ======
# Strip spaces from column names
df.columns = df.columns.str.strip()

# ====== 4. NULL VALUE CHECK ======
null_summary = df.isnull().sum().reset_index()
null_summary.columns = ["column", "missing_values"]
null_summary.to_csv(os.path.join(output_dir, "null_values_summary.csv"), index=False)
print("Null values summary saved.")

# ====== 5. INTERACTION TYPE ANALYSIS ======
if "interaction_type" in df.columns:
    interaction_counts = df["interaction_type"].value_counts().reset_index()
    interaction_counts.columns = ["interaction_type", "count"]
    interaction_counts.to_csv(os.path.join(output_dir, "interaction_type_counts.csv"), index=False)
    print("Interaction type counts saved.")
else:
    print("Skipped: 'interaction_type' column not found.")

# ====== 6. CHANNEL & SOURCE ANALYSIS ======
for col in ["channel", "source_channel"]:
    if col in df.columns:
        counts = df[col].value_counts().reset_index()
        counts.columns = [col, "count"]
        counts.to_csv(os.path.join(output_dir, f"{col}_counts.csv"), index=False)
        print(f"{col} counts saved.")
    else:
        print(f"Skipped: '{col}' column not found.")

# ====== 7. DEVICE TYPE ANALYSIS ======
if "device_type" in df.columns:
    device_counts = df["device_type"].value_counts().reset_index()
    device_counts.columns = ["device_type", "count"]
    device_counts.to_csv(os.path.join(output_dir, "device_type_counts.csv"), index=False)
    print("Device type counts saved.")
else:
    print("Skipped: 'device_type' column not found.")

# ====== 8. LEAD QUALITY SCORE STATS ======
if "lead_quality_score" in df.columns:
    score_stats = df["lead_quality_score"].describe().reset_index()
    score_stats.columns = ["statistic", "value"]
    score_stats.to_csv(os.path.join(output_dir, "lead_quality_score_stats.csv"), index=False)
    print("Lead quality score stats saved.")
else:
    print("Skipped: 'lead_quality_score' column not found.")

# ====== 9. CONVERSION ANALYSIS ======
if "converted" in df.columns:
    overall_conversion = df["converted"].value_counts(normalize=True) * 100
    overall_conversion.to_csv(os.path.join(output_dir, "conversion_rates.csv"))

    if "channel" in df.columns:
        conversion_by_channel = df.groupby("channel")["converted"].mean() * 100
        conversion_by_channel.to_csv(os.path.join(output_dir, "conversion_by_channel.csv"))
    print("Conversion analysis saved.")
else:
    print("Skipped: 'converted' column not found.")

# ====== 10. TIME-BASED ANALYSIS ======
if "created_at" in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    leads_per_month = df.groupby(df["created_at"].dt.to_period("M")).size().reset_index(name="count")
    leads_per_month.to_csv(os.path.join(output_dir, "leads_per_month.csv"), index=False)
    print("Leads per month analysis saved.")
else:
    print("Skipped: 'created_at' column not found.")

print(f"\nRegeneration complete. Processed CSVs saved in: {output_dir}")

