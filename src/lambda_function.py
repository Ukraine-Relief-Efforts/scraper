import logging
import sys

sys.path.insert(0, "./deps")

# Additional imports
from scrapers.poland import PolandScraper
from scrapers.moldova_ro import MoldovaScraper
from scrapers.hungary_hu import HungaryScraper
from scrapers.romaina_ro import RomaniaScraper

poland_scraper = PolandScraper()
hungary_scraper = HungaryScraper()
moldova_scraper = MoldovaScraper()
romania_scraper = RomaniaScraper()


def lambda_handler(event, context):
    """Call all scrapers."""

    if "country" in event:
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
        elif country == "romania-ro":
            romania_scraper.scrape(event)
    else:
        for scraper in [
            poland_scraper,
            hungary_scraper,
            moldova_scraper,
            romania_scraper,
        ]:
            try:
                scraper.scrape(event)
            except Exception:
                logging.exception("An error was encountered during scraping.")
