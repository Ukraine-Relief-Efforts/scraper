import os
import requests
from pykml import parser as Kml
from utils.reception import Reception
from utils.constants import HEADERS, OUTPUT_DIR
from utils.utils import get_website_content, write_to_json, normalize

HUNGARY_URL = "https://www.police.hu/hu/hirek-es-informaciok/hatarinfo/hataratlepessel-kapcsolatos-informaciok"
HUNGARY_KML = "http://www.google.com/maps/d/kml?forcekml=1&mid=1d54nWG4ig0rmBPj3K3RF3I1mkY0KOFZd"

def scrape_hungary_hu():
  """Start with general border info"""
  content = get_website_content(HUNGARY_URL)
  core = get_general(content)

  """Get border crossing points"""
  reception_arr = get_reception_points()
  path = os.path.join(OUTPUT_DIR, 'hungary_hu.json')
  write_to_json(path, core, reception_arr, HUNGARY_URL)


def get_general(content):
  """Gets general border crossing information."""
  main_div = content.find('div', class_="field-szovegtorzs oldal")
  items = main_div.findAll('p')
  text_arr = []
  for item in items:
    text_arr.append(normalize(item.get_text(strip=True, separator=' ')))
  return text_arr


def get_reception_points():
  """Get map KML"""
  kml_str = requests.get(HUNGARY_KML, headers=HEADERS).content
  kml = Kml.fromstring(kml_str)

  """Only interested in the border crossing folder"""
  folders = kml.Document.findall('.//{http://www.opengis.net/kml/2.2}Folder')
  for folder in folders:
    name = normalize(folder.name.text)
    if "Border crossing point" in name:
      return get_placemarks(folder)

  return []

def get_placemarks(folder):
  """Find all placemarks"""
  recep_arr = []
  placemarks = folder.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
  for placemark in placemarks:
    """Skip petrol stations"""
    if placemark.styleUrl.text == "#icon-1581-E65100" or placemark.styleUrl.text == "#icon-1581-F57C00-nodesc":
      continue

    r = Reception()
    r.name = normalize(placemark.name.text)
    coord = placemark.Point.coordinates.text.split(',')
    r.lon = coord[0].strip()
    r.lat = coord[1].strip()
    recep_arr.append(r)

  return recep_arr
