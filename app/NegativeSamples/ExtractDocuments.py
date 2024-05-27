import json

from mzkscraper.Scraper import MZKScraper

scraper = MZKScraper()

# GET ALL VALID DOCUMENTS
query = scraper.get_search_query(access="open", licenses="public", doctypes="sheetmusic")
document_ids = scraper.get_search_results(query, pages="all")

with open("app/NegativeSamples/documents.json", "w", encoding="utf8") as f:
    json.dump(document_ids, f, indent=4)
