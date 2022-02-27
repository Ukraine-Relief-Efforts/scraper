import requests
import xmltodict

from utils.constants import HEADERS
from utils.dynamo import write_to_dynamo
from utils.utils import get_reception_points, get_website_content, normalize

HUNGARY_URL = "https://www.police.hu/hu/hirek-es-informaciok/hatarinfo/hataratlepessel-kapcsolatos-informaciok"
HUNGARY_KML = "http://www.google.com/maps/d/kml?forcekml=1&mid=1d54nWG4ig0rmBPj3K3RF3I1mkY0KOFZd"


def scrape_hungary_hu():
    print("Scraping Hungary (HU)")

    """Start with general border info"""
    content = get_website_content(HUNGARY_URL)
    general = get_general(content)

    """Get border crossing points"""
    reception_arr = _get_reception_points()
    write_to_dynamo("hungary-hu-test", general, reception_arr, HUNGARY_URL)


def get_general(content):
    """Gets general border crossing information."""
    main_div = content.find('div', class_="field-szovegtorzs oldal")
    items = main_div.findAll('p')
    text_arr = []
    for item in items:
        text_arr.append(normalize(item.get_text(strip=True, separator=' ')))
    return text_arr


def _get_reception_points():
    """Get map KML"""
    kml_str = requests.get(HUNGARY_KML, headers=HEADERS).content
    kml = xmltodict.parse(kml_str, dict_constructor=dict)
    return get_reception_points(
        kml=kml,
        folder_name_whitelist=["Border crossing point"],
        style_urls_blacklist=["#icon-1581-E65100", "#icon-1581-F57C00-nodesc"],
    )
