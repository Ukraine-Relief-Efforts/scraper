import os
import requests
from bs4 import BeautifulSoup
from utils.reception import Reception
from utils.constants import POLAND_EN_URL, HEADERS, OUTPUT_DIR
from utils.utils import write_to_json, normalize


"""Runs the scraping logic."""
def scrape_poland_en():
  content = get_website_content()
  core = get_core(content)
  reception_arr = get_reception_points(content)
  path = os.path.join(OUTPUT_DIR, 'poland_en.json')
  write_to_json(path, core, reception_arr, POLAND_EN_URL)

"""Gets the website content with BS4."""
def get_website_content():
  website = requests.get(POLAND_EN_URL, headers=HEADERS)
  return BeautifulSoup(website.content, 'html.parser')


"""Gets the content from a bullet points list of general information for Ukrainian citizens."""
def get_core(content):
  items = content.find('div', class_="editor-content").find("div").findAll("span")
  text_arr = []
  for item in items:
    if item.find(text="RECEPTION POINT ADDRESS"):
      break
    text_arr.append(normalize(item.get_text(strip=True, separator=' ')))
  return text_arr


"""Gets the list of reception points."""
def get_reception_points(soup):
  items = soup.find('div', class_="editor-content").find('div').findChildren(recursive=False)
  reception_list_start = False
  recep_arr = []
  count = 0

  for item in items:

    if item.find(text="RECEPTION POINT ADDRESS"):
      reception_list_start = True
      continue
    elif item.find(text="What next?"):
      break

    if reception_list_start:
      count += 1
      # special case
      if count == 1:
        r = Reception()
        r.location = normalize(item.get_text(strip=True, separator=' '))
        gmaps = item.find('a', href=True)
        
        if gmaps:
          r.gmaps = gmaps['href']
        img = item.find('img', src=True)
        if img:
          r.qr = img['src']
        recep_arr.append(r)
        continue

      # normal case
      if count % 2 == 0:
        r = Reception()
        r.location = normalize(item.get_text(strip=True, separator=' '))
        gmaps = item.find('a', href=True)
        if gmaps:
          r.gmaps = gmaps['href']
          recep_arr.append(r)
      else:
        # Get from the end of array,
        img = item.find('img', src=True)
        if img:
          recep_arr[-1].qr = img['src']

  return recep_arr
