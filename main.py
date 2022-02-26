
from pathlib import Path
from scrapers.poland import scrape_poland_pl, scrape_poland_en, scrape_poland_ua
from scrapers.moldova_ro import scrape_moldova_ro
from scrapers.hungary_hu import scrape_hungary_hu
from utils.constants import OUTPUT_DIR

if __name__=="__main__":
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    print("Scraping Poland (PL)")
    scrape_poland_pl()
    print("Scraping Poland (EN)")
    scrape_poland_en()
    print("Scraping Poand (UA)")
    scrape_poland_ua()

    print("Scraping Moldova (RO)")
    scrape_moldova_ro()

    print("Scraping Hungary (HU)")
    scrape_hungary_hu()
    
