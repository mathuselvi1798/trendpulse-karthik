# task2_data_processing.py
# TrendPulse - Task 2: Load the raw JSON from Task 1, clean it with
# Pandas, and save the tidy result as a CSV file.

import os
import glob

import pandas as pd

# ---------------------------------------------------------------
# Step 1 - Load the JSON file into a DataFrame
# ---------------------------------------------------------------

# Task 1 saves files named like data/trends_YYYYMMDD.json.
# glob finds all of them; sorting puts the newest date last,
# so we pick the most recent file automatically.
json_files = sorted(glob.glob("data/trends_*.json"))

if not json_files:
    print("No JSON file found in data/. Run task1_data_collection.py first.")
    raise SystemExit

json_path = json_files[-1]

# read_json turns the list of story objects into rows and columns
df = pd.read_json(json_path)
print(f"Loaded {len(df)} stories from {json_path}\n")

# ---------------------------------------------------------------
# Step 2 - Clean the data
# ---------------------------------------------------------------

# 2a. Duplicates: keep only the first row for each post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2b. Missing values: a story is useless without an ID, title, or score
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 2c. Data types: score and num_comments must be whole numbers.
# num_comments can be missing for very new stories, so fill those
# with 0 first; otherwise converting to int would fail.
df["num_comments"] = df["num_comments"].fillna(0)
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 2d. Low quality: drop stories with fewer than 5 upvotes
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 2e. Whitespace: remove extra spaces at the start/end of titles
df["title"] = df["title"].str.strip()

# ---------------------------------------------------------------
# Step 3 - Save as CSV and print a summary
# ---------------------------------------------------------------

os.makedirs("data", exist_ok=True)
csv_path = "data/trends_clean.csv"

# index=False stops Pandas from writing its row numbers as a column
df.to_csv(csv_path, index=False)
print(f"\nSaved {len(df)} rows to {csv_path}\n")

# Count stories in each category (sort=False keeps the original order)
print("Stories per category:")
category_counts = df["category"].value_counts(sort=False)
for category, count in category_counts.items():
    print(f"  {category:<15} {count}")