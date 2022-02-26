from scrapers.poland import scrape_poland_pl, scrape_poland_en, scrape_poland_ua
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
        3: "PL_UA",
        4: "MD_MD",
        5: "HU_HU"
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
        scrape_poland_ua()
        scrape_moldova_ro()
        scrape_hungary_hu()

    if switch_country(country) == "PL_PL":
        scrape_poland_pl()

    if switch_country(country) == "PL_EN":
        scrape_poland_en()

    if switch_country(country) == "PLA_UA":
        scrape_poland_ua()

    if switch_country(country) == "MD_MD":
        scrape_moldova_ro()

    if switch_country(country) == "HU_HU":
        scrape_hungary_hu()
