import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import inflection

from .ImageData import ImageData, ImageDataEncoder

from pathlib import Path


class MZKScraper:
    VALID_LABELS = [
        "frontCover",
        "FrontCover",

        "frontEndSheet",
        "FrontEndSheet",

        "blank",

        "backEndSheet",
        "BackEndSheet",

        "backCover",
        "BackCover",

        "titlePage",
        "TitlePage",

        "backEndPaper",

        "tableOfContents",
        "TableOfContents",

        "index",
        "Index",

        "frontEndPaper",
        "FrontEndPaper",

        "Illustration",
        "illustration",

        "fragmentsOfBookbinding",  # 29e3938f-bc72-4ec1-aeec-d54d908a99b0
        "FragmentsOfBookbinding",
    ]
    INVALID_LABELS = [
        "sheetmusic",
        "calibrationTable",

        "FlyLeaf",
        "flyLeaf",

        "normalPage",
        "NormalPage",

        "spine",
        "Spine",  # b57d0175-adf7-4c86-bb52-0c3e02aa35ee

        "edge",
        "Edge",  # 97df2260-d12c-4fe1-9b41-d511744366d5

        "cover",  # 37c18f61-cb2e-4d49-90c4-a25df0b00850
    ]

    iiif_request_url = "https://iiif.digitalniknihovna.cz/mzk/uuid:"

    @staticmethod
    def scrape_for_class(url, timeout: float = 60,
                         search_for: str = "ng-star-inserted",
                         wait_for=(By.CLASS_NAME, "app-card-content-wrapper")):
        try:
            # initialize a headless browser with Selenium
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('--log-level=3')
            driver = webdriver.Chrome(options=options)

            # load page
            driver.get(url)

            # wait for dynamic loading
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(wait_for)
            )

            # parse html
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            ng_star_inserted_elements = soup.find_all(class_=search_for)

            # search for href attributes
            href_list = [element.get("href") for element in ng_star_inserted_elements]

            return href_list
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            driver.quit()

    @staticmethod
    def _clean_up_hrefs(hrefs: list[str | None]) -> list[str]:
        output = []
        for href in hrefs:
            if href is not None and "uuid" in href:
                output.append(href.split(":")[1])
        return output

    @staticmethod
    def _strip_page_label(label: str) -> str:
        return label.split(" ")[1].replace("(", " ").replace(")", "").replace(" ", "")

    @staticmethod
    def _get_image_id(img_json: dict) -> str:
        return img_json["thumbnail"][0]["id"].split("uuid:")[1].split("/")[0]

    def get_specified_pages(self, page_info: dict[str, str]) -> list[ImageData]:
        output = []
        doc_id = page_info["id"]
        for sheet in page_info["items"]:
            labels = sheet["label"]["none"]
            if len(labels) > 1:
                print("Warning: more labels then expected:", labels)
            else:
                try:
                    label = self._strip_page_label(labels[0])
                    if label not in self.VALID_LABELS and label not in self.INVALID_LABELS:
                        print("New found label:", label)
                        print(self._get_image_id(sheet))
                    if label in self.VALID_LABELS:
                        output.append(ImageData(doc_id, self._get_image_id(sheet), inflection.underscore(label)))
                except IndexError:
                    continue

        return output

    def load_search_results(self, query: str, page_count: int = 1,
                            timeout: float = 60) -> list[str]:
        """
        Given a search query to MZK loads the query and searches for documents inside this page. MZK search results
        are loaded dynamically.

        Parameters
        :param query: Search query to MZK
        :param page_count: Number of pages to load
        :param timeout: Timeout in seconds, if method doesn't return anything try to increase this timeout
        :return: List of found documents IDs
        """
        if "page" not in query:
            query += "&page={page_num}"

        MAX_RESULT_PER_PAGE = 60  # there are 60 documents for each page of search results
        all_docs = []
        page_num = 1
        while page_num <= page_count:
            hrefs = self.scrape_for_class(query.format(page_num=page_num), timeout=timeout)
            hrefs = self._clean_up_hrefs(hrefs)
            if len(hrefs) == 0:
                print(f"No results found at page number {page_num}\nat {query.format(page_num=page_num)}. Quitting job")
                break
            elif len(hrefs) < MAX_RESULT_PER_PAGE:
                print(f"Warning: Found less results than expected. Expected {MAX_RESULT_PER_PAGE}, got {len(hrefs)}. "
                      f"At page {page_num}\nat {query.format(page_num=page_num)} ")
            all_docs += hrefs
            page_num += 1

        return all_docs

    def load_pages_in_document(self, doc_id: str) -> list[ImageData] | None:
        """
        Sends request to MZK using IIIF and parses information about all pages inside a document.
        Returns list of `ImageData` objects. If request fails, returns `None`.

        Parameters
        :param doc_id: Document ID
        :return: List of `ImageData` objects or None, if request fails
        """
        page_data = get_json_from_url(self.iiif_request_url + doc_id)
        if page_data is not None:
            return self.get_specified_pages(page_data)
        else:
            return None


def get_json_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print(f"Error: Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
