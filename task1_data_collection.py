# task1_data_collection.py
# TrendPulse - Task 1: Fetch trending stories from the HackerNews API,
# assign each story a category using title keywords, and save to JSON.

import os
import json
import time
from datetime import datetime

import requests

# ---------------------------------------------------------------
# Settings
# ---------------------------------------------------------------

BASE_URL = "https://hacker-news.firebaseio.com/v0"

# Header required by the assignment
HEADERS = {"User-Agent": "TrendPulse/1.0"}

MAX_IDS = 500               # fetch the first 500 IDs from each list
MAX_PER_CATEGORY = 25       # up to 25 stories per category (125 total)

# Story lists to read from, in order.
# "topstories" is the main source required by the task. Top stories
# alone often don't have enough world news / sports / science titles,
# so if categories are still not full, we also check "beststories"
# and "newstories" as backup sources.
STORY_LISTS = ["topstories", "beststories", "newstories"]

# Keywords for each category (matching is case-insensitive).
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer",
                   "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president",
                  "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team",
               "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology",
                "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game",
                      "book", "show", "award", "streaming"],
}


# ---------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------

def fetch_json(url):
    """Send a GET request and return the parsed JSON.
    If anything goes wrong, print a message and return None
    so the script keeps running instead of crashing."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()   # raises an error for 4xx/5xx codes
        return response.json()
    except requests.RequestException as error:
        print(f"Request failed for {url}: {error}")
        return None


def get_matching_categories(title):
    """Return a list of ALL categories whose keywords appear in the title.
    A title can match more than one category (e.g. 'game' is in both
    sports and entertainment)."""
    title_lower = title.lower()       # lowercase so matching ignores case
    matches = []
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                matches.append(category)
                break                 # one keyword is enough for this category
    return matches


def all_categories_full(stories_by_category):
    """True when every category already has 25 stories."""
    return all(len(stories) >= MAX_PER_CATEGORY
               for stories in stories_by_category.values())


# ---------------------------------------------------------------
# Step 1 & 2 - Fetch story IDs, then each story's details
# ---------------------------------------------------------------

# One list of collected stories per category
stories_by_category = {category: [] for category in CATEGORIES}

# Remember which IDs we already checked, because the same story
# can appear in more than one list (top, best, new)
seen_ids = set()

for list_name in STORY_LISTS:
    # Stop early if every category is already full
    if all_categories_full(stories_by_category):
        break

    print(f"Fetching story IDs from '{list_name}'...")
    story_ids = fetch_json(f"{BASE_URL}/{list_name}.json")
    if not story_ids:
        continue                      # this list failed, try the next one

    story_ids = story_ids[:MAX_IDS]
    print(f"Got {len(story_ids)} IDs. Fetching story details...")

    for count, story_id in enumerate(story_ids, start=1):
        if all_categories_full(stories_by_category):
            break

        if story_id in seen_ids:
            continue                  # already checked this story
        seen_ids.add(story_id)

        story = fetch_json(f"{BASE_URL}/item/{story_id}.json")

        # Skip failed requests, deleted items, and items without a title
        if not story or "title" not in story:
            continue

        # Put the story in the first matching category that still has
        # room. This way, a story isn't wasted just because its first
        # matching category is already full, and no story is counted twice.
        for category in get_matching_categories(story["title"]):
            if len(stories_by_category[category]) < MAX_PER_CATEGORY:
                # Save only the 7 required fields.
                # .get() with a default avoids errors when a field is
                # missing (new stories may have no "descendants" yet).
                stories_by_category[category].append({
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
                break

        # Small progress message every 100 stories
        if count % 100 == 0:
            total_so_far = sum(len(s) for s in stories_by_category.values())
            print(f"  {list_name}: processed {count}/{len(story_ids)}, "
                  f"collected {total_so_far} so far")

# ---------------------------------------------------------------
# Step 3 - Build the final list, category by category
# ---------------------------------------------------------------

all_stories = []
for category, stories in stories_by_category.items():
    all_stories.extend(stories)
    print(f"{category}: {len(stories)} stories")

    # One 2-second pause per category loop (not per story), as required
    time.sleep(2)

# ---------------------------------------------------------------
# Step 4 - Save everything to data/trends_YYYYMMDD.json
# ---------------------------------------------------------------

os.makedirs("data", exist_ok=True)            # create data/ if missing

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
with open(filename, "w", encoding="utf-8") as file:
    json.dump(all_stories, file, indent=4, ensure_ascii=False)

print(f"Collected {len(all_stories)} stories. Saved to {filename}")