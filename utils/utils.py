import json
import logging
from utils.constants import LOGFILE_PATH
import unicodedata

"""Normalizes the provided text. This is needed to get rid of weird entries like \xa0."""
def normalize(text):
  return unicodedata.normalize("NFKD", text)

def write_to_json(filename, text_arr, reception_arr, source):
  reception = []
  for rec in reception_arr:
    reception.append({
      "qr": rec.qr_url,
      "gmaps": rec.gmaps,
      "address": rec.location,
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