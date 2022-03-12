import logging

import requests
import xmltodict

from scrapers.base_scraper import BaseScraper
from utils.constants import HEADERS
from utils.dynamo import write_to_dynamo
from utils.utils import get_reception_points, get_website_content, normalize

MOLDOVA_UKRAINE_URL = "https://www.border.gov.md/ro/ucraina"
MOLDOVA_KML = (
    "http://www.google.com/maps/d/kml?forcekml=1&mid=1S38hHlp67u7UoFgVGFC-GCU2Efsn6WeC"
)


class MoldovaScraper(BaseScraper):
    def scrape(self, event=""):
        logging.info("Scraping Moldova (RO)")

        """Start with general border info"""
        content = get_website_content(MOLDOVA_UKRAINE_URL)
        general = self.get_general(content)

        """Get border crossing points"""
        reception_arr = self._get_reception_points()
        write_to_dynamo(
            "moldova-ro", event, general, reception_arr, MOLDOVA_UKRAINE_URL
        )

    def get_general(self, content):
        """Gets general border crossing information."""
        main_div = content.find("div", class_="col-lg-10 offset-lg-1")
        items = main_div.findAll("p")
        text_arr = []
        for item in items:
            text_arr.append(normalize(item.get_text(strip=True, separator=" ")))
        return text_arr

    def _get_reception_points(self):
        """Gets the list of reception points."""

        """Get map KML"""
        kml_str = requests.get(MOLDOVA_KML, headers=HEADERS).content
        kml = xmltodict.parse(kml_str, dict_constructor=dict)
        return get_reception_points(kml=kml)
