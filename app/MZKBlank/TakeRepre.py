import json
import math
import random

with open("app/MZKBlank/scraped_data/pages.json", "r", encoding="utf8") as f:
    data = json.load(f)

total = data["count"]
max_repre = 1_000

# get count for each class
sample_count = []
for key, value in data.items():
    if key == "count":
        continue

    sample_count.append(math.ceil(value['count'] / total * max_repre))

# choose random pages to represent
i = 0
for key, value in data.items():
    if key == "count":
        continue

    chosen_indices = random.sample(range(0, value["count"]), k=sample_count[i])
    chosen_pages = [value["items"][chosen_indices[i]] for i in range(len(chosen_indices))]
    value["items"] = chosen_pages
    value["count"] = sample_count[i]
    i += 1

data["count"] = sum(sample_count)

# reassign IDs
unique_id = 0
for key, value in data.items():
    if key == "count":
        continue

    for page in value["items"]:
        page["id"] = unique_id
        unique_id += 1

# save data
with open("app/MZKBlank/scraped_data/chosen.json", "w", encoding="utf8") as f:
    json.dump(data, f, indent=4)
