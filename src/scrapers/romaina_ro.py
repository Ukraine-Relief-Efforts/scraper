from scrapers.base_scraper import BaseScraper
from utils.dynamo import write_to_dynamo
from utils.reception import Reception
from utils.utils import get_website_content, gmaps_url_to_lat_lon, normalize

ROMANIA_INFO_URL = "https://www.politiadefrontiera.ro/ro/main/pg-conditii-generale-de-calatorie-a-cetatenilor-din-statele-care-nu-sunt-membre-ale-uniunii-europene-si-spatiului-economic-european-147.html"
ROMANIA_MAP_URL = "https://www.politiadefrontiera.ro/ro/traficonline/?dt=1&vw=2"


class RomaniaScraper(BaseScraper):
    def scrape(self, event=""):
        print("Scraping Romania (RO)")

        """Start with general border info"""
        content = get_website_content(ROMANIA_INFO_URL)
        general = self.get_general(content)

        """Get border crossing points"""
        reception_arr = self._get_reception_points(ROMANIA_MAP_URL)
        write_to_dynamo("romania-ro", event, general, reception_arr, ROMANIA_INFO_URL)

    def get_general(self, content):
        """Gets general border crossing information."""
        main_div = content.find("div", class_="mrow txtcontent")
        items = main_div.findAll("p")
        text_arr = []
        for item in items:
            text_arr.append(normalize(item.get_text(strip=True, separator=" ")))
        return text_arr

    def _get_reception_points(self, url):
        recep_arr = []
        content = get_website_content(url)

        """Get a list of table rows"""
        main_div = content.find("div", class_="txtcontent")
        rows = main_div.findAll("tr")

        """Get crossing info from each table row cell"""
        for row in rows:
            """Skip table header row"""
            if row.find("th") is not None:
                continue

            cells = row.findAll("td")

            """Parse cell content into Reception object"""
            r = Reception()
            r.name = normalize(cells[0].find("span").get_text(strip=True))
            # wait_time = cells[1]
            # info = cells[2]
            gmaps = cells[3].find("a", href=True)
            r.lat, r.lon = gmaps_url_to_lat_lon(gmaps["href"])
            recep_arr.append(r)

        return recep_arr
