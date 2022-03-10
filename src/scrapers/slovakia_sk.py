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
    "Pravidelne aktualizované informácie o situácii na slovenských hraniciach nájdete na Facebooku Polície SR a Ministerstva vnútra SR.",
    "Občania Ukrajiny s biometrickým pasom môžu na Slovensko vstúpiť v rámci bezvízového styku a zdržiavať sa na Slovensku bez víz maximálne 90 dní v akomkoľvek 180-dňovom období.",
    "Podľa informácií Ministerstva vnútra SR (tlačová správa TU, informácia na Facebooku TU) je momentálne vstup umožnený všetkým osobám, ktoré utekajú pred vojnovým konfliktom. Vstup na územie Slovenskej republiky sa po individuálnom posúdení umožňuje aj osobám, ktoré nemajú platný cestovný doklad (biometrický pas, prípadne vízum).",
    "Osoby prichádzajúce zo susedného štátu, v ktorom boli bezprostredne pred príchodom vystavené ohrozeniu počas ozbrojeného konfliktu a osoby, ktoré potrebujú medzinárodnú ochranu alebo cestujú z iných humanitárnych dôvodov spĺňajú podmienky vstupu na Slovensko stanovené v súvislosti s pandémiou koronavírusu.",
    "Pri príchode na Slovensko sa tieto osoby nemusia registrovať na stránke http://korona.gov.sk/ehranica a nevzťahuje sa na nich ani povinnosť izolácie. ",
    "Po vstupe na územie SR je potrebné hlásiť začiatok pobytu do 3 pracovných dní od vstupu – formulár na stiahnutie a bližšie informácie tu https://www.minv.sk/?hlasenie-pobytu-1",
    "Všetkým osobám, ktoré utekajú pred vojnovým konfliktom a ktorým bol umožnený vstup cez slovenskú hrancicu (spravidla majú v pase vstupnú slovenskú pečiatku), je umožnený krátkodobý pobyt do 90 dní.",
    "Viac informácií nájdete tu: https://www.mic.iom.sk/en/news/758-info-ukraine.html (en) https://www.mic.iom.sk/sk/novinky/757-info-ukrajina.html (sk)",
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
