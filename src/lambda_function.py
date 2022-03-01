import sys

sys.path.insert(0, "./deps")

# Additional imports
from scrapers.poland import PolandScraper
from scrapers.moldova_ro import MoldovaScraper
from scrapers.hungary_hu import HungaryScraper
from scrapers.romaina_ro import RomaniaScraper
from utils.utils import log_to_discord, LogLevelEnum, DiscordLogData

poland_scraper = PolandScraper()
hungary_scraper = HungaryScraper()
moldova_scraper = MoldovaScraper()
romania_scraper = RomaniaScraper()


def lambda_handler(event, context):
    """Call all scrapers."""

    scrapers = []

    if "country" in event:
        country = event["country"]
        if country == "poland-en":
            scrapers.append((country, poland_scraper.scrape_poland_en))
        elif country == "poland-pl":
            scrapers.append((country, poland_scraper.scrape_poland_pl))
        elif country == "poland-ua":
            scrapers.append((country, poland_scraper.scrape_poland_ua))
        elif country == "hungary-hu":
            scrapers.append((country, hungary_scraper.scrape))
        elif country == "moldova-ro":
            scrapers.append((country, moldova_scraper.scrape))
        elif country == "romania-ro":
            scrapers.append((country, romania_scraper.scrape))
    else:
        scrapers = [
            ("poland-[all]", poland_scraper.scrape),
            ("hungary-[all]", hungary_scraper.scrape),
            ("moldova-[all]", moldova_scraper.scrape),
            ("romania-[all]", romania_scraper.scrape),
        ]

    scraper_outcomes: list[tuple[str, str]] = []
    for scraper_name, scraper_function in scrapers:
        try:
            scraper_function(event)
        except Exception as exception:
            scraper_outcomes.append((scraper_name, str(exception)))
        else:
            scraper_outcomes.append((scraper_name, "Success!"))

    log = DiscordLogData(
        title="TEST scraper log event",
        description="\n".join(f"{t[0]} -- {t[1]}" for t in scraper_outcomes),
        log_level=LogLevelEnum.INFO
    )
    log_to_discord(logs=[log])
