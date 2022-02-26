from scrapers.poland_pl import scrape_poland_pl
from scrapers.poland_en import scrape_poland_en
from scrapers.moldova_ro import scrape_moldova_ro

if __name__=="__main__":
    print("Scraping Poland (PL)")
    scrape_poland_pl()
    print("Scraping Poland (EN)")
    scrape_poland_en()

    print("Scraping Moldova (RO)")
    scrape_moldova_ro()
    