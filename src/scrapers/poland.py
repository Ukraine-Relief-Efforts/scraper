from scrapers.base_scraper import BaseScraper
from utils.reception import Reception
from utils.utils import get_website_content, gmaps_url_to_lat_lon, normalize
from utils.dynamo import write_to_dynamo

POLAND_PL_URL = "https://www.gov.pl/web/udsc/ukraina2"
POLAND_PL_RECEPTION_URL = "https://www.gov.pl/web/udsc/punkty-recepcyjne2"

# Keeping these ULRs around as a backup incase they are ever needed
# POLAND_EN_URL = "https://www.gov.pl/web/udsc/ukraina-en"
# POLAND_UA_URL = "https://www.gov.pl/web/udsc/ukraina---ua"


class PolandScraper(BaseScraper):
    def scrape(self, event=""):
        self.scrape_poland_pl(event)
        # self.scrape_poland_ua(event)
        # self.scrape_poland_en(event)

    def scrape_poland_pl(self, event=""):
        print("Scraping Poland (PL)")

        """calls scrape_poland with the appropriate arguments for the pl website"""
        self.scrape_poland(POLAND_PL_URL, "pl", event)

    # def scrape_poland_ua(self, event=""):
    #     print("Scraping Poand (UA)")

    #     """calls scrape_poland with the appropriate arguments for the ua website"""
    #     self.scrape_poland(POLAND_UA_URL, "ua", event)

    # def scrape_poland_en(self, event=""):
    #     print("Scraping Poland (EN)")

    #     """calls scrape_poland with the appropriate arguments for the en website"""
    #     self.scrape_poland(POLAND_EN_URL, "en", event)

    def get_core(self, content, locale):
        """Gets the content from a bullet points list of general information for Ukrainian citizens."""
        items = content.find("div", class_="editor-content").findAll(
            "span" if locale == "en" else "li"
        )
        text_arr = []
        for item in items:
            if item.find(text="RECEPTION POINT ADDRESS"):
                break
            text_arr.append(normalize(item.get_text(strip=True, separator=" ")))
        return text_arr

    def scrape_poland(self, url, locale, event):
        """Runs the scraping logic."""
        content = get_website_content(url)
        general = self.get_core(content, locale)
        if locale in (
            "pl",
            "ua",
        ):  # poland_ua doesn't seem to have a reception points URL, might change though. For now, grab the polish one and hope the translator doesn't mess up
            reception_arr = self.get_reception_points_pl(
                get_website_content(POLAND_PL_RECEPTION_URL)
            )
        elif locale == "en":
            reception_arr = self.get_reception_points_en(content)

        country = "poland-" + locale
        write_to_dynamo(country, event, general, reception_arr, url)

    def get_reception_points_en(self, soup):
        """Gets the list of reception points."""
        items = (
            soup.find("div", class_="editor-content")
            .find("div")
            .findChildren(recursive=False)
        )
        reception_list_start = False
        recep_arr = []
        count = 0

        for item in items:
            # start scraping for reception points after the title
            if item.find(text="RECEPTION POINT ADDRESS"):
                reception_list_start = True
                continue
            # stop scraping after "what's next?"
            if item.find(text="What next?"):
                break

            if not reception_list_start:
                continue

            count += 1
            r = Reception()
            r.address = r.name = normalize(item.get_text(strip=True, separator=" "))
            gmaps = item.find("a", href=True)

            if gmaps:
                if "!3d" in gmaps["href"]:
                    r.lat, r.lon = gmaps_url_to_lat_lon(gmaps["href"])
                else:
                    break

            img = item.find("img", src=True)

            # first item is special because the qr and address are in the same <p> tag
            if count == 1:
                if img:
                    r.qr = img["src"]
                recep_arr.append(r)
                continue

            # normal items: qr and address are in separate <p> tags
            if count % 2 == 0:
                recep_arr.append(r)
            else:
                # Get from the end of array,
                img = item.find("img", src=True)
                if img:
                    recep_arr[-1].qr = img["src"]

        return recep_arr

    def get_reception_points_pl(self, soup):
        """Gets the list of reception points."""
        # TODO no QR codes
        # TODO maybe this is not the best way of going about things. please double check, I'm tired
        maindiv = soup.find("div", class_="editor-content")
        recep_arr = []

        for val in maindiv.find_all("a"):
            recep = Reception()
            recep.address = recep.name = normalize(
                val.get_text(strip=True, separator=" ")
            )
            gmaps = val["href"]
            if gmaps and "!3d" in gmaps:
                recep.lat, recep.lon = gmaps_url_to_lat_lon(gmaps)
            else:
                continue  # TODO what to do when the lat/lon isn't in the URL?
            recep_arr.append(recep)
        return recep_arr
