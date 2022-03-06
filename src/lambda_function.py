import logging
from concurrent.futures import ThreadPoolExecutor

from loggy import init_logging
from scrapers.hungary_hu import HungaryScraper
from scrapers.moldova_ro import MoldovaScraper
from scrapers.poland import PolandScraper
from scrapers.romaina_ro import RomaniaScraper
from utils.utils import DiscordLogData, LogLevelEnum, log_to_discord

init_logging()

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
        scraper_outcomes: list[tuple[str, str]] = []

        def run_scraper(scraper):
            try:
                scraper.scrape(event)
            except Exception as exception:
                outcome = (scraper.__class__.__name__, str(exception))
                scraper_outcomes.append(outcome)
                logging.exception(
                    "Failed running scraper: %s", scraper.__class__.__name__
                )
                raise exception
            else:
                outcome = (scraper.__class__.__name__, "Success!")
                scraper_outcomes.append(outcome)
                logging.info("Successfully ran scraper: %s", scraper.__class__.__name__)

        with ThreadPoolExecutor(4) as pool:
            results = pool.map(run_scraper, scrapers)

        log = DiscordLogData(
            title="TEST scraper log event",
            description="\n".join(f"{t[0]} -- {t[1]}" for t in scraper_outcomes),
            log_level=LogLevelEnum.INFO,
        )
        log_to_discord(logs=[log])

        # Convert the iterator to a list in case any of them raised exceptions
        _ = list(results)
