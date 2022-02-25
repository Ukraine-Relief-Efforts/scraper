from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()


class Reception:
    def __init__(self):
        self._location = ""
        self._qr_url = ""
        self._gmaps = ""

    def __str__(self):
        nl = '\n'
        return f"Location: {self._location}{nl} QR: {self.qr_url}{nl} GMaps:{self._gmaps}{nl}===="

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, loc):
        self._location = loc

    @property
    def qr_url(self):
        return self._qr_url

    @qr_url.setter
    def qr_url(self, qr):
        self._qr_url = qr

    @property
    def gmaps(self):
        return self._gmaps

    @qr_url.setter
    def gmaps(self, qr):
        self._gmaps = qr


def get_core(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    item = soup.find('div', class_="editor-content").findAll('li')
    text_arr = []
    for i in item:
        text_arr.append(i.get_text(strip=True, separator=' '))
    return text_arr


def fetch_site():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
    r = requests.get('https://www.gov.pl/web/udsc/ukraina2', headers=headers)
    text_arr = get_core(r)
    print(text_arr)
    reception_arr = fetch_reception_points(r)
    for i in reception_arr:
        print(i)
        return i


def write_to_json():
    pass


def fetch_reception_points(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    item = soup.find('div', class_="editor-content").findAll('p')
    item = item[1:]

    recep_arr = []
    """
    First one looks like this
    
    <p><span style="font-size:11pt"><u><span style="font-size:10.5pt"><span style="color:blue"><a href="https://www.google.pl/maps/place/Gminny+Ośrodek+Kultury+i+Turystyki/@51.1653246,23.8026394,17z/data=!3m1!4b1!4m5!3m4!1s0x4723890b09b9cd4d:0x5747c0a6dfbbb992!8m2!3d51.1653213!4d23.8048281"><span style="color:blue">Pałac Suchodolskich Gminny Ośrodek Kultury i Turystyki, ul. Parkowa 5, 22-175 </span><strong>Dorohusk – osiedle</strong></a></span></span></u><br>
<img alt="https://www.qr-online.pl/bin/qr/8caf19812112ea544f35e994cd58573c.png" height="102" src="https://www.qr-online.pl/bin/qr/8caf19812112ea544f35e994cd58573c.png" width="102"/> ​</br></span></p>
    
    Rest of the things look like this
    
    <p><span style="font-size:11pt"><u><span style="color:blue"><a href="https://www.google.pl/maps/place/Sp%C3%B3%C5%82dzielcza+8,+22-540+Do%C5%82hobycz%C3%B3w/@50.5879307,24.0283211,17z/data=!3m1!4b1!4m5!3m4!1s0x4724ebc1d634e40b:0xd5f90534ea38bc2!8m2!3d50.5879273!4d24.0305098"><span style="color:blue">Przygraniczne Centrum Kultury i Rekreacji, ul. Spółdzielcza 8, 22 - 540 </span><strong>Dołhobyczów</strong></a></span></u></span></p>
=====
<p><span style="font-size:11pt"><img alt="https://www.qr-online.pl/bin/qr/7608a0a9319f79f95fb5346d5f6e3466.png" height="110" src="https://www.qr-online.pl/bin/qr/7608a0a9319f79f95fb5346d5f6e3466.png" width="110"/> ​</span></p>

  Temporarily hardcoding for the first one
    
  """
    special_case = item[0]
    r = Reception()
    r.location = special_case.get_text(strip=True, separator=' ')
    gmaps = special_case.find('a', href=True)

    if gmaps:
        r.gmaps = gmaps['href']
    img = special_case.find('img', src=True)
    if img:
        r.qr_url = img['src']
    recep_arr.append(r)
    item.pop(0)
    # TODO: Remove the entire above block if and when they fix the formatting on the site.

    count = 0
    for i in item:
        if count % 2 == 0:
            r = Reception()
            r.location = i.get_text(strip=True, separator=' ')
            gmaps = i.find('a', href=True)
            if gmaps:
                r.gmaps = gmaps['href']
                recep_arr.append(r)
        else:
            # Get from the end of array,
            img = i.find('img', src=True)
            if img:
                recep_arr[-1].qr_url = img['src']

        count += 1
    return recep_arr


@app.get("/")
def root():
    result = fetch_site()
    return result


if __name__ == "__main__":
    fetch_site()
