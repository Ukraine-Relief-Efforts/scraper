import logging
import sys
from concurrent.futures import ThreadPoolExecutor

from scrapers.hungary_hu import HungaryScraper
from scrapers.moldova_ro import MoldovaScraper
# Additional imports
from scrapers.poland import PolandScraper
from scrapers.romaina_ro import RomaniaScraper

sys.path.insert(0, "./deps")


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
        scrapers = [
            poland_scraper,
            hungary_scraper,
            moldova_scraper,
            romania_scraper,
        ]

        def run_scraper(scraper):
            try:
                scraper.scrape(event)
            except Exception:
                logging.exception("An error was encountered during scraping.")
                raise

        with ThreadPoolExecutor(4) as pool:
            results = pool.map(run_scraper, scrapers)
        # Convert the iterator to a list in case any of them raised exceptions
        _ = list(results)
