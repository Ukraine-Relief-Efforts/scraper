import sys

sys.path.insert(0, './deps')

# from moldova_ro import scrape_moldova_ro
from poland import scrape_poland_pl, scrape_poland_en


def lambda_handler(event, context):
    """Call all scrapers."""
    print("Scraping Poland")
    scrape_poland_pl()
    scrape_poland_en()

    # print("Scraping Moldova")
    # scrape_moldova_ro()
