import json

from mzkscraper.Scraper import MZKScraper

scraper = MZKScraper()

# GET ALL VALID DOCUMENTS
query = scraper.construct_solr_query_with_qf(access="open", licences="public", doctypes="sheetmusic")
document_ids = scraper.retrieve_document_ids_by_solr_query(query, requested_document_count="all")

with open("app/MZKBlank/scraped_data/documents.json", "w", encoding="utf8") as f:
    json.dump(document_ids, f, indent=4)
