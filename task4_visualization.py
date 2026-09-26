# task4_visualization.py
# TrendPulse - Task 4: Load the analysed CSV from Task 3, draw charts
# with Matplotlib, save each one as a PNG, and build a combined dashboard.

import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Step 1 - Setup
# ---------------------------------------------------------------

csv_path = "data/trends_analysed.csv"
df = pd.read_csv(csv_path)
print(f"Loaded data: {df.shape}")

# Create the outputs folder if it does not exist yet
os.makedirs("outputs", exist_ok=True)


def short_title(text, limit=50):
    """Cut long titles so they fit on the chart."""
    text = str(text)
    return text if len(text) <= limit else text[:limit - 3] + "..."


# ---------------------------------------------------------------
# Step 2 - Chart 1: Top 10 stories by score (horizontal bar)
# ---------------------------------------------------------------

top10 = df.sort_values("score", ascending=False).head(10)
labels = [short_title(t) for t in top10["title"]]

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(labels, top10["score"], color="steelblue")
ax1.invert_yaxis()  # highest score at the top
ax1.set_title("Top 10 Stories by Score")
ax1.set_xlabel("Score")
ax1.set_ylabel("Story")
fig1.tight_layout()
fig1.savefig("outputs/chart1_top_stories.png")
plt.close(fig1)
print("Saved outputs/chart1_top_stories.png")

# ---------------------------------------------------------------
# Step 3 - Chart 2: Number of stories per category (bar)
# ---------------------------------------------------------------

category_counts = df["category"].value_counts()
colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
          "#937860", "#DA8BC3", "#8C8C8C"]

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.bar(category_counts.index, category_counts.values,
        color=colors[:len(category_counts)])
ax2.set_title("Stories per Category")
ax2.set_xlabel("Category")
ax2.set_ylabel("Number of Stories")
fig2.tight_layout()
fig2.savefig("outputs/chart2_categories.png")
plt.close(fig2)
print("Saved outputs/chart2_categories.png")

# ---------------------------------------------------------------
# Step 4 - Chart 3: Score vs comments (scatter, popular vs not)
# ---------------------------------------------------------------

# is_popular may load as text "True"/"False", so convert it safely
popular_mask = df["is_popular"].astype(str).str.lower() == "true"
popular = df[popular_mask]
not_popular = df[~popular_mask]

fig3, ax3 = plt.subplots(figsize=(8, 6))
ax3.scatter(not_popular["score"], not_popular["num_comments"],
            color="gray", alpha=0.6, label="Not popular")
ax3.scatter(popular["score"], popular["num_comments"],
            color="orange", alpha=0.8, label="Popular")
ax3.set_title("Score vs Number of Comments")
ax3.set_xlabel("Score")
ax3.set_ylabel("Number of Comments")
ax3.legend()
fig3.tight_layout()
fig3.savefig("outputs/chart3_scatter.png")
plt.close(fig3)
print("Saved outputs/chart3_scatter.png")

# ---------------------------------------------------------------
# Step 5 - Dashboard: all three charts in one figure
# ---------------------------------------------------------------

fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("TrendPulse Dashboard", fontsize=16)

# Panel 1 - top 10 stories
axes[0].barh([short_title(t, 30) for t in top10["title"]],
             top10["score"], color="steelblue")
axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")

# Panel 2 - stories per category
axes[1].bar(category_counts.index, category_counts.values,
            color=colors[:len(category_counts)])
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(axis="x", rotation=30)

# Panel 3 - score vs comments
axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                color="gray", alpha=0.6, label="Not popular")
axes[2].scatter(popular["score"], popular["num_comments"],
                color="orange", alpha=0.8, label="Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

fig.tight_layout()
fig.savefig("outputs/dashboard.png")
print("Saved outputs/dashboard.png")

# Show the dashboard window (close it to finish the script)
plt.show()
