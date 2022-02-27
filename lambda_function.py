import sys

sys.path.insert(0, "./deps")

from scrapers.poland import PolandScraper
from scrapers.moldova_ro import MoldovaScraper
from scrapers.hungary_hu import HungaryScraper

poland_scraper = PolandScraper()
hungary_scraper = HungaryScraper()
moldova_scraper = MoldovaScraper()

testSuffix = ""

def lambda_handler(event, context):
    """Call all scrapers."""
    #######################################################################################################################################
    # USED FOR TESTING IN LAMBDA. Include 'testSuffix' in your lambda test object so that the dynamo items used in prod are not overwritten
    testSuffix = "" if ('testSuffix' not in event) else event["testSuffix"]
    #######################################################################################################################################

    if 'country' in event:
        country = event["country"]
        if country == "poland-en":
            poland_scraper.scrape_poland_en()
        elif country == "poland-pl":
            poland_scraper.scrape_poland_pl()
        elif country == "poland-ua":
            poland_scraper.scrape_poland_ua()
        elif country == "hungary-hu":
            hungary_scraper.scrape()
        elif country == "moldova-ro":
            moldova_scraper.scrape()
    else:
        poland_scraper.scrape()
        hungary_scraper.scrape()
        moldova_scraper.scrape()
