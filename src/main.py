from scrapers.poland import PolandScraper
from scrapers.moldova_ro import MoldovaScraper
from scrapers.hungary_hu import HungaryScraper
from scrapers.romaina_ro import RomaniaScraper

#
# Country switch.
#
def switch_country(country):
    country_switch = {
        0: "ALL",
        1: "PL_PL",
        2: "PL_EN",
        3: "PL_UA",
        4: "MD_MD",
        5: "HU_HU",
        6: "RO_RO"
    }

    return country_switch.get(country, "ALL")

if __name__=="__main__":
    #
    # Default value which is 'ALL'.
    #
    country = 0
    poland_scraper = PolandScraper()
    hungary_scraper = HungaryScraper()
    moldova_scraper = MoldovaScraper()
    romania_scraper = RomaniaScraper()

    if switch_country(country) == "ALL":
        poland_scraper.scrape()
        hungary_scraper.scrape()
        moldova_scraper.scrape()
        romania_scraper.scrape()

    if switch_country(country) == "PL_PL":
        poland_scraper.scrape_poland_pl()

    if switch_country(country) == "PL_EN":
        poland_scraper.scrape_poland_en()

    if switch_country(country) == "PLA_UA":
        poland_scraper.scrape_poland_ua()

    if switch_country(country) == "MD_MD":
        moldova_scraper.scrape()

    if switch_country(country) == "HU_HU":
        hungary_scraper.scrape()
    
    if switch_country(country) == "RO_RO":
        romania_scraper.scrape()

