import sys

sys.path.insert(0, "./deps")

from scrapers.poland import PolandScraper
from scrapers.moldova_ro import MoldovaScraper
from scrapers.hungary_hu import HungaryScraper

poland_scraper = PolandScraper()
hungary_scraper = HungaryScraper()
moldova_scraper = MoldovaScraper()


def lambda_handler(event, context):
    """Call all scrapers."""
    poland_scraper.scrape_poland_en()
    poland_scraper.scrape_poland_pl()
    poland_scraper.scrape_poland_ua()
    hungary_scraper.scrape()
    moldova_scraper.scrape()
