import json
import logging
import unicodedata
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from utils.constants import LOGFILE_PATH, HEADERS
from utils.reception import Reception


def normalize(text):
    """Normalizes the provided text. This is needed to get rid of weird entries like \xa0."""
    return unicodedata.normalize("NFKD", text)


def get_website_content(url, headers=HEADERS):
    """Gets the website content with BS4."""
    website = requests.get(url, headers=headers)
    return BeautifulSoup(website.content, "html.parser")


def get_reception_points(
    kml: dict,
    folder_name_whitelist=None,
    style_urls_blacklist=None,
):
    if style_urls_blacklist is None:
        style_urls_blacklist = []
    reception_points: list[Reception] = []
    folders = kml["kml"]["Document"]["Folder"]
    for folder in folders:
        if folder_name_whitelist is None or any(
            value in normalize(folder["name"]) for value in folder_name_whitelist
        ):
            if "Placemark" in folder.keys():
                for placemark in folder["Placemark"]:
                    if placemark["styleUrl"] not in style_urls_blacklist:
                        r = Reception()
                        r.name = normalize(placemark["name"])
                        coord = placemark["Point"]["coordinates"].split(",")
                        r.lon = coord[0].strip()
                        r.lat = coord[1].strip()
                        reception_points.append(r)
    return reception_points


def gmaps_url_to_lat_lon(url):
    """Converts a Google maps URL string into latitude and longitude."""
    if "!3d" in url:
        return url.split("!3d")[1].split("!4d")
    else:
        return url.split("/")[6].split(",")


def write_to_json(filename, text_arr, reception_arr, source):
    reception = []
    for rec in reception_arr:
        reception.append(
            {
                "name": rec.name,
                "lat": rec.lat,
                "lon": rec.lon,
                "address": rec.address,
                "qr": rec.qr,
            }
        )
    data = {"general": text_arr, "reception": reception, "source": source}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def setup_logger():
    LOGGER = logging.getLogger("scraper")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        handlers=[
            logging.FileHandler(LOGFILE_PATH, "a", "utf-8"),
            logging.StreamHandler(),
        ],
    )
    return LOGGER


def log_to_discord(scraper_outcomes: list[tuple[str, str]]):
    url = "https://discord.com/api/webhooks/948021922661281883/IT9C3Q1ITRH4A_VUdfz8bYLLDum_qSY0c_BcNUlLebIgW1SLBKkxW5CZFNzfVvMQK5a0"
    content = {
        "content": None,
        "embeds": [
            {
                "title": datetime.utcnow().isoformat(),
                "description": "\n".join(f"{t[0]} -- {t[1]}" for t in scraper_outcomes),
                "color": None
            }
        ]
    }
    requests.post(url, json=content)
