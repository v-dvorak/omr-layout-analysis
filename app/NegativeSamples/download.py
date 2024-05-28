from mzkscraper.Scraper import MZKScraper
from pathlib import Path
from tqdm import tqdm
import json

# load data
with open("app/NegativeSamples/scraped_data/chosen.json", "r", encoding="utf8") as f:
    data = json.load(f)

scraper = MZKScraper()
OUTPUT_DIR = Path("datasets/NegativeSamples/img")
if OUTPUT_DIR.exists():
    print("Dataset already downloaded.")
    quit()

for key, value in tqdm(list(data.items())):
    if key == "count":
        continue

    for page in value["items"]:
        scraper.download_image(page["img_id"], f"{key}_{page['id']}.png", OUTPUT_DIR)
