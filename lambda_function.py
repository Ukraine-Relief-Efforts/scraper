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

    if 'country' in event:
        country = event["country"]
        if country == "poland-en":
            poland_scraper.scrape_poland_en(event)
        elif country == "poland-pl":
            poland_scraper.scrape_poland_pl(event)
        elif country == "poland-ua":
            poland_scraper.scrape_poland_ua(event)
        elif country == "hungary-hu":
            hungary_scraper.scrape(event)
        elif country == "moldova-ro":
            moldova_scraper.scrape(event)
    else:
        poland_scraper.scrape(event)
        hungary_scraper.scrape(event)
        moldova_scraper.scrape(event)
