import logging

from scrapers.base_scraper import BaseScraper
from utils.dynamo import write_to_dynamo
from utils.reception import Reception
from utils.utils import get_website_content

SLOVAKIA_URL = "https://www.minv.sk/?hranicne-priechody-1"

class SlovakiaScraper(BaseScraper):
    def scrape(self, event=""):
        content = None
        general = self._get_general(content)
        reception_arr = self._get_reception_points(content)
        write_to_dynamo("slovakia-sk", event, general, reception_arr, SLOVAKIA_URL)

    def _get_general(self, content):
        return ["this is a test 1", "this is a test 2", "t3", "t4", "t5", "t6"]

    def _get_reception_points(self, content):
        return [
            Reception("name", "address", "no qr lol", "69", "420"),
            Reception("name2", "address2", "no qr lol", "69.420", "420.69"),
            Reception("name3", "address3", "no qr lol", "69.420", "420.69"),
            Reception("name4", "address5", "no qr lol", "69.420", "420.69"),
            Reception("name5", "address6", "no qr lol", "69.420", "420.69"),
            Reception("name6", "address8", "no qr lol", "69.420", "420.69"),
            Reception("name7", "address69", "no qr lol", "69.420", "420.69"),
        ]
