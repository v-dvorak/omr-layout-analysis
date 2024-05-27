from tqdm import tqdm
import json
import time

from mzkscraper.Scraper import MZKScraper
from mzkscraper.PageData import PageDataEncoder

with open("app/NegativeSamples/valid_labels.json", "r", encoding="utf8") as f:
    labels = json.load(f)

VALID_LABELS = labels["VALID_LABELS"]

scraper = MZKScraper()

# GET PAGES FROM DOCUMENTS
with open("app/NegativeSamples/documents.json", "r", encoding="utf8") as f:
    document_ids = json.load(f)

output = {
    "count": 0
}

MAX_RETRIES = 3
BACKOFF_START = 1  # in seconds
BACKOFF_MULTIPLIER = 2

unique_id = 0
for document_id in tqdm(document_ids):
    retries = MAX_RETRIES - 1
    pages = scraper.get_pages_in_document(document_id, VALID_LABELS)
    backoff = BACKOFF_START
    while pages is None and retries > 0:
        time.sleep(backoff)
        print("Trying again.")
        pages = scraper.get_pages_in_document(document_id, VALID_LABELS)
        retries -= 1
        backoff *= BACKOFF_MULTIPLIER
    if retries == 0:
        print(f"Failed for all {MAX_RETRIES} retries.")
    try:
        for page in pages:
            output["count"] += 1

            page.system_id = unique_id
            unique_id += 1

            if page.label in output.keys():
                output[page.label]["items"].append(page)
                output[page.label]["count"] += 1
            else:
                output[page.label] = {
                    "count": 1,
                    "items": [page]
                }
    except Exception as e:
        print(e)

with open(f"app/NegativeSamples/pages.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, cls=PageDataEncoder)
