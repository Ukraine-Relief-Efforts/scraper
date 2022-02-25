import requests
from bs4 import BeautifulSoup

class Reception():
  def __init__(self):
    self.__location = ""
    self.__qr_url = ""
    self.__gmaps = ""

    

def get_core(r):
  soup = BeautifulSoup(r.content, 'html.parser')
  item = soup.find('div', class_="editor-content").findAll('li')
  text_arr = []
  for i in item:
    text_arr.append(i.get_text(strip=True, separator=' '))
  return text_arr

def fetch_site():
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
  r = requests.get('https://www.gov.pl/web/udsc/ukraina2', headers=headers)
  text_arr = get_core(r)
  print(text_arr)
  reception_arr = fetch_reception_points(r)
  print(reception_arr)

def write_to_json():
  pass

def fetch_reception_points(r):
  soup = BeautifulSoup(r.content, 'html.parser')
  item = soup.find('div', class_="editor-content").findAll('p')
  item = item[1:]
  text_arr = []
  for i in item:
    text_arr.append(i.get_text(strip=True, separator=' '))
  return text_arr
  
fetch_site()
