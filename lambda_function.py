import sys

sys.path.insert(0, './deps')

from scrapers.poland import scrape_poland_pl, scrape_poland_en, scrape_poland_ua
from scrapers.hungary_hu import scrape_hungary_hu
from scrapers.moldova_ro import scrape_moldova_ro


def lambda_handler(event, context):
    """Call all scrapers."""
    scrape_poland_pl()
    scrape_poland_en()
    scrape_poland_ua()
    scrape_hungary_hu()
    scrape_moldova_ro()
