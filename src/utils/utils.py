import json
import logging
import unicodedata
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from utils.constants import HEADERS, LOGFILE_PATH
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
                        r.address = r.name  # TEMPORARY
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


class LogLevelEnum(Enum):
    INFO = 562741
    DEBUG = 10227
    WARN = 16240465
    ERROR = 15942656


@dataclass()
class DiscordLogData:
    title: str
    description: str
    log_level: LogLevelEnum


def log_to_discord(logs: list[DiscordLogData]):
    try:
        with open(Path(__file__).parent / ".discord-webhook", "r") as file:
            url = file.read().strip()
        if len(logs) > 10:
            raise ValueError("Discord supports a maximum of 10 embeds per message")
        content = {
            "content": None,
            "embeds": [
                {
                    "title": log.title,
                    "description": log.description,
                    "color": log.log_level.value,
                }
                for log in logs
            ],
        }
        requests.post(url, json=content)
    except Exception as exception:
        # Don't fail execution if logging fails
        logging.exception("Failed to send Discord notification.")
