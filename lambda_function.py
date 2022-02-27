import sys
from scrapers.poland import PolandScraper
from scrapers.moldova_ro import MoldovaScraper
from scrapers.hungary_hu import HungaryScraper
from scrapers.romaina_ro import RomaniaScraper

sys.path.insert(0, './deps')

def lambda_handler(event, context):
    """Call all scrapers."""
    poland_scraper = PolandScraper()
    poland_scraper.scrape()

    hungary_scraper = HungaryScraper()
    hungary_scraper.scrape()

    moldova_scraper = MoldovaScraper()
    moldova_scraper.scrape()

    romania_scraper = RomaniaScraper()
    romania_scraper.scrape()
