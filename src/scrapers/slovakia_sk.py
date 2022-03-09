import logging
import requests
import xmltodict

from scrapers.base_scraper import BaseScraper
from utils.dynamo import write_to_dynamo
from utils.reception import Reception
from utils.utils import get_website_content, normalize
from utils.constants import HEADERS

# not used for some reason
# TODO use it to get addresses?
# SLOVAKIA_URL = "https://www.minv.sk/?hranicne-priechody-1"

SLOVAKIA_GENERAL_URL = "https://www.minv.sk/?tlacove-spravy&sprava=vstup-na-slovensko-bez-povinnosti-karanteny"
SLOVAKIA_KML = (
    "https://www.google.com/maps/d/kml?forcekml=1&mid=1umLgEK-j5BHcJAvRBZMFtWztNzhWwgoP"
)

# Hard code this because:
#    1) the website is annoying
#    2) it would be hard to automatically edit it down because there's tonnes of unnecesary information
# Source: https://www.mic.iom.sk/en/news/758-info-ukraine.html
HARD_CODED_GENERAL = [
    "Regularly updated information on the situation at the Slovak border can be found on the Facebook pages of the Slovak Police and the Slovak Ministry of the Interior.",
    "Citizens of Ukraine with a biometric passport can enter Slovakia under the visa-free regime and stay in Slovakia without a visa for a maximum of 90 days in any 180-day period.",
    "According to information from the Ministry of Interior of the Slovak Republic  entry is currently allowed to all persons fleeing the conflict. Upon individual assessment, entry will be allowed also to persons who do not have a valid travel document (biometric passport, visa).",
    "Persons arriving from a neighbouring country where they have been exposed to a threat during an armed conflict immediately prior to their arrival and persons in need of international protection or travelling for other humanitarian reasons meet the conditions for entry to Slovakia set out in the context of a coronavirus pandemic.",
    "They do not need to register at http://korona.gov.sk/ehranica when they arrive in Slovakia and are not subject to the isolation obligation.",
    "After entering Slovakia, it is necessary to report the beginning of your stay within 3 business days – a relevant form to download and more information at https://www.minv.sk/?reporting-residence-1",
    "All persons fleeing the conflict who have been allowed entry through the Slovak border (usually with a Slovak entry stamp in their passport) are allowed a short-term stay of up to 90 days.",
    "More information can be found here: https://www.mic.iom.sk/en/news/758-info-ukraine.html",
]


class SlovakiaScraper(BaseScraper):
    def scrape(self, event=""):
        logging.info("Scraping Slovakia (SK)")
        general = self._get_general()
        reception_arr = self._get_reception_points()
        write_to_dynamo(
            "slovakia-sk", event, general, reception_arr, SLOVAKIA_GENERAL_URL
        )

    def _get_general(self):
        content = get_website_content(SLOVAKIA_GENERAL_URL)
        target_text = "Zmeny v súvislosti s aktuálnym dianím na  Ukrajine"
        antitarget_text = (
            "Vstup na Slovensko bez karantény podmienený súhlasom ministerstva vnútra"
        )
        finding = False
        data = []
        for tag in list(content.find(id="main-content"))[0]:
            if tag.name == "h3" and str(tag.string) == antitarget_text:
                finding = False
            if finding:
                data.append(" ".join(tag.stripped_strings))
            if tag.name == "h3" and str(tag.string) == target_text:
                finding = True

        data = [n for n in data if n]
        data.extend(HARD_CODED_GENERAL)
        return data

    def _get_reception_points(self) -> list[Reception]:
        # stolen from https://github.com/Aziroshin/scraper/commits/master
        kml_str = requests.get(SLOVAKIA_KML, headers=HEADERS).content
        kml = xmltodict.parse(kml_str, dict_constructor=dict)

        # A modified copy of `get_reception_points` which, for now, works with
        # KML file "v3". There's still stuff missing, though (e.g. address).
        # What works: Using Mali Selmentsi as an example, lat & long seems to
        # work at least.
        reception_points: list[Reception] = []
        placemarks: List = kml["kml"]["Document"]["Folder"]["Placemark"]
        for placemark in placemarks:
            r = Reception()
            r.name = normalize(placemark["name"])
            r.address = r.name  # TODO temporary
            coord = placemark["Point"]["coordinates"].split(",")
            r.lon = coord[0].strip()
            r.lat = coord[1].strip()
            reception_points.append(r)

        return reception_points
