from mzkscraper.Scraper import MZKScraper
from pathlib import Path
from tqdm import tqdm
import json

# load data
with open("app/NegativeSamples/chosen.json", "r", encoding="utf8") as f:
    data = json.load(f)

scraper = MZKScraper()

for key, value in tqdm(list(data.items())):
    if key == "count":
        continue

    for page in value["items"]:
        scraper.download_image(page["img_id"], f"{key}_{page['id']}.png", Path("datasets/NegativeSamples/images"))
