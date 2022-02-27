import json
import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup
from utils.constants import LOGFILE_PATH, HEADERS
import unicodedata

from utils.reception import Reception


def normalize(text):
  """Normalizes the provided text. This is needed to get rid of weird entries like \xa0."""
  return unicodedata.normalize("NFKD", text)

def get_website_content(url, headers=HEADERS):
  """Gets the website content with BS4."""
  website = requests.get(url, headers=headers)
  return BeautifulSoup(website.content, 'html.parser')

def get_reception_points(
        kml: dict,
        folder_name_whitelist: Optional[list[str]]=None,
        style_urls_blacklist: Optional[list[str]]=None,
):
  if style_urls_blacklist is None:
    style_urls_blacklist = []
  reception_points: list[Reception] = []
  folders = kml["kml"]["Document"]["Folder"]
  for folder in folders:
    if folder_name_whitelist is None or any(
            value in normalize(folder["name"])
            for value in folder_name_whitelist
    ):
      if "Placemark" in folder.keys():
        for placemark in folder["Placemark"]:
          if placemark["styleUrl"] not in style_urls_blacklist:
            r = Reception()
            r.name = normalize(placemark["name"])
            coord = placemark["Point"]["coordinates"].split(',')
            r.lon = coord[0].strip()
            r.lat = coord[1].strip()
            reception_points.append(r)
  return reception_points

def gmaps_url_to_lat_lon(url):
  """Converts a Google maps URL string into latitude and longitude."""
  return url.split("!3d")[1].split("!4d")

def write_to_json(filename, text_arr, reception_arr, source):
  reception = []
  for rec in reception_arr:
    reception.append({
      "name": rec.name,
      "lat": rec.lat,
      "lon": rec.lon,
      "address": rec.address,
      "qr": rec.qr,
    })
  data = {"general": text_arr, "reception": reception, "source": source}
  with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

def setup_logger():
  LOGGER = logging.getLogger("scraper")
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        logging.FileHandler(LOGFILE_PATH, 'a', 'utf-8'),
        logging.StreamHandler()
    ]
  )
  return LOGGER
