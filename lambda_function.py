import sys

sys.path.insert(0, './deps')

# from moldova_ro import scrape_moldova_ro
from poland_en import scrape_poland_en
from poland_pl import scrape_poland_pl


def lambda_handler(event, context):
    """Call all scrapers."""
    
    print("Scraping Poland (PL)")
    scrape_poland_pl()

    print("Scraping Poland (EN)")
    scrape_poland_en()

    # print("Scraping Moldova (RO)")
    # scrape_moldova_ro()

