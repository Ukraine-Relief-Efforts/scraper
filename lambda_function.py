import sys

sys.path.insert(0, './deps')

from scrapers.poland import scrape_poland_pl, scrape_poland_en
from scrapers.poland_pl import scrape_poland_pl
from scrapers.poland_en import scrape_poland_en
from scrapers.hungary_hu import scrape_hungary_hu
from scrapers.moldova_ro import scrape_moldova_ro


def lambda_handler(event, context):
    """Call all scrapers."""
    print("Scraping Poland (PL)")
    scrape_poland_pl()

    print("Scraping Poland (EN)")
    scrape_poland_en()

    print("Scraping Hungary (HU)")
    scrape_hungary_hu()

    print("Scraping Moldova (RO)")
    scrape_moldova_ro()
