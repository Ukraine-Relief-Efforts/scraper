from scrapers.poland_pl import scrape_poland_pl
from scrapers.poland_en import scrape_poland_en
from scrapers.moldova_ro import scrape_moldova_ro
from scrapers.hungary_hu import scrape_hungary_hu

#
# Country switch.
#
def switch_country(country):
    country_switch = {
        0: "ALL",
        1: "PL_PL",
        2: "PL_EN",
        3: "MD_MD",
        4: "HU_HU"
    }

    return country_switch.get(country, "ALL")

if __name__=="__main__":
    #
    # Default value which is 'ALL'.
    #
    country = 0

    if switch_country(country) == "ALL":
        scrape_poland_pl()
        scrape_poland_en()
        scrape_moldova_ro()
        scrape_hungary_hu()

    if switch_country(country) == "PL_PL":
        scrape_poland_pl()

    if switch_country(country) == "PL_EN":
        scrape_poland_en()

    if switch_country(country) == "MD_MD":
        scrape_moldova_ro()

    if switch_country(country) == "HU_HU":
        scrape_hungary_hu()