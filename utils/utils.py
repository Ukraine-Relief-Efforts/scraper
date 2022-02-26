import json
import logging
from pickle import FALSE
import requests
from bs4 import BeautifulSoup
from utils.constants import LOGFILE_PATH, HEADERS
import unicodedata

"""Normalizes the provided text. This is needed to get rid of weird entries like \xa0."""
def normalize(text):
  return unicodedata.normalize("NFKD", text)

"""Gets the website content with BS4."""
def get_website_content(url, headers=HEADERS):
  website = requests.get(url, headers=headers)
  return BeautifulSoup(website.content, 'html.parser')

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