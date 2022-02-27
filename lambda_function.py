import sys

sys.path.insert(0, './deps')

from scrapers.poland import scrape_poland_pl, scrape_poland_en
from scrapers.poland_en import scrape_poland_en
from scrapers.hungary_hu import scrape_hungary_hu
from scrapers.moldova_ro import scrape_moldova_ro


def lambda_handler(event, context):
    """Call all scrapers."""
    scrape_poland_pl()
    scrape_poland_en()
    scrape_hungary_hu()
    scrape_moldova_ro()
