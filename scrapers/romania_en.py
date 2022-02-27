from collections import defaultdict
from PIL import Image
from pytesseract import image_to_string

from bs4 import *
import requests
import os

from scrapers.base_scraper import BaseScraper
from utils.dynamo import write_to_dynamo
from utils.reception import Reception

ROMANIA_EN_URL = "https://romania.iom.int/news/useful-information-people-entering-romania-ukraine"
BASE_URL = "https://romania.iom.int"


class RomaniaScraper(BaseScraper):
    def __init__(self):
        self._image_downloader = ImageDownloader(ROMANIA_EN_URL, BASE_URL)
        self.mapping = defaultdict(Reception)
        self.mapping["Halmeu"] = Reception("Halmeu", "Halmeu", "", "47.99949245007817", "23.001865588674413")
        self.mapping["Sighetu Marmatiei"] = Reception("Sighetu Marmatiei", "Sighetu Marmatiei", "", "47.9389198",
                                                      "23.8775945")
        self.mapping["Siret"] = Reception("Siret", "Siret", "", "47.987979983510925", "26.061198978070973")
        self.mapping["Isaccea"] = Reception("Isaccea", "Siret", "", "45.28398915528812", "28.453329592029377")

    def scrape(self):
        self._image_downloader.run()
        text = self.decode_text_from_image()
        border_crossings = self.find_border_crossings(text)
        reception_list = list()
        for border in border_crossings:
            reception_list.append(self.mapping[border])
        write_to_dynamo("Romania", "Border crossing pointsś", reception_list, "")

    def decode_text_from_image(self) -> str:
        for file in os.scandir("temp"):
            try:
                image = Image.open(file.path)
            except:
                continue
            result_string = image_to_string(image)
            if result_string.find("cross into Romania") != -1:
                return result_string

    def find_border_crossings(self, text: str):
        text_of_interest = "points can be used to cross into Romania:"
        text_beginning_pos = text.find(text_of_interest) + len(text_of_interest)
        text_end_pos = text.find("+", text_beginning_pos)
        if text_end_pos == -1:
            text_end_pos = text.find("*", text_beginning_pos)
        border_points = text[text_beginning_pos: text_end_pos].replace('\n', '')
        border_points = border_points.split(',')
        return border_points


class ImageDownloader:
    def __init__(self, url: str, base_url: str):
        self._url = url
        self._base_url = base_url
        self._folder_name = "temp"
        pass

    def folder_create(self, images):
        try:
            os.mkdir(self._folder_name)
        except:
            pass

    def download_images(self, images, folder_name):
        if len(images) == 0:
            return

        possible_tags = ["data-srcset", "data-src", "data-fallback-src", "src"]
        for i, image in enumerate(images):
            for tag in possible_tags:
                try:
                    image_link = image[tag]
                except:
                    continue
            try:
                r = requests.get(self._base_url + image_link).content
                with open(f"{folder_name}/images{i + 1}.jpg", "wb+") as f:
                    f.write(r)
            except:
                pass

    def run(self):
        r = requests.get(self._url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.findAll('img')
        self.folder_create(images)
        self.download_images(images, self._folder_name)
