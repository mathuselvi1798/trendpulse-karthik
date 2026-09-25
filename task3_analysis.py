# task3_analysis.py
# TrendPulse - Task 3: Load the clean CSV from Task 2, explore it,
# compute statistics with NumPy, add two new columns, and save the result.

import pandas as pd
import numpy as np

# ---------------------------------------------------------------
# Step 1 - Load and explore
# ---------------------------------------------------------------

csv_path = "data/trends_clean.csv"
df = pd.read_csv(csv_path)

# shape gives (number of rows, number of columns)
print(f"Loaded data: {df.shape}\n")

print("First 5 rows:")
print(df.head())

# Pandas .mean() gives a quick average for each column
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()
print(f"\nAverage score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

# ---------------------------------------------------------------
# Step 2 - Basic analysis with NumPy
# ---------------------------------------------------------------

# Convert columns to NumPy arrays so we can use NumPy functions
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()
categories = df["category"].to_numpy()
titles = df["title"].to_numpy()

print("\n--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):,.0f}")
print(f"Median score : {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score    : {np.max(scores):,}")
print(f"Min score    : {np.min(scores):,}")

# np.unique with return_counts=True gives each category and how
# many times it appears; argmax finds the position of the biggest count
unique_categories, category_counts = np.unique(categories, return_counts=True)
top_index = np.argmax(category_counts)
print(f"\nMost stories in: {unique_categories[top_index]} "
      f"({category_counts[top_index]} stories)")

# argmax on the comments array gives the row with the most comments
most_commented = np.argmax(comments)
print(f'\nMost commented story: "{titles[most_commented]}" '
      f"— {comments[most_commented]:,} comments")

# ---------------------------------------------------------------
# Step 3 - Add new columns
# ---------------------------------------------------------------

# engagement = discussion per upvote.
# We add 1 to score so we never divide by zero.
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True when a story scores above the average score
df["is_popular"] = df["score"] > np.mean(scores)

# ---------------------------------------------------------------
# Step 4 - Save the result
# ---------------------------------------------------------------

output_path = "data/trends_analysed.csv"
# index=False keeps Pandas row numbers out of the file
df.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")