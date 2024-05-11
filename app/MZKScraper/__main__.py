from .Scraper import MZKScraper


# MZK Scraper showcase

url = "https://www.digitalniknihovna.cz/mzk/search?access=open&licences=public&doctypes=sheetmusic&page={page_num}"
scraper = MZKScraper()

# load documents that satisfy search query
res = scraper.load_search_results(url, timeout=60)
print(*res, sep="\n")

# load valid images from first document
print(*scraper.load_pages_in_document(res[0]), sep="\n")
