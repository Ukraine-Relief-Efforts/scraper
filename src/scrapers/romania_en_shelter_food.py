from bs4 import *
import requests
import os

from PIL import Image
from pytesseract import image_to_string
from geopy.geocoders import Nominatim

from scrapers.base_scraper import BaseScraper
from utils.dynamo import write_to_dynamo
from utils.reception import Reception
from itertools import permutations


ROMANIA_EN_URL = (
    "https://romania.iom.int/news/useful-information-people-entering-romania-ukraine"
)
BASE_URL = "https://romania.iom.int"


class RomaniaRefugeeCenterScraper(BaseScraper):
    def __init__(self):
        self._image_downloader = ImageDownloader(ROMANIA_EN_URL, BASE_URL)

    def scrape(self):
        event = ""
        self._image_downloader.run()
        text = self.decode_text_from_image()
        general = self.find_general_information(text)
        border_crossings = self.find_refugee_centers(text)
        write_to_dynamo(
            "shelter-food-romania-en", event, [general], border_crossings, ""
        )

    def find_general_information(self, text: str):
        text_of_interest = "Seeking Asylum"
        text_beginning_pos = text.find(text_of_interest)
        text_end_pos = text.find("Accommodation in Asylum")
        general_information = text[text_beginning_pos:text_end_pos]
        general_information = general_information.replace("\n\n", "\n")
        return general_information

    def find_refugee_centers(self, text: str):
        text_of_interest = "Accommodation in Asylum"
        text_beginning_pos = text.find(text_of_interest)
        text_beginning_pos = text.find("*", text_beginning_pos)
        text_end_pos = text.find("For information", text_beginning_pos)
        refugee_points = text[text_beginning_pos:text_end_pos].split("*")
        reception_list = list()
        geolocator = Nominatim(user_agent="Ukraine-relief-effort")
        for refugee_point in refugee_points:
            reception_point = Reception()
            first_index = refugee_point.find(":")
            if first_index == -1:
                continue
            last_index = refugee_point.find("/ Phone", first_index)
            reception_point.name = refugee_point[0:first_index].replace("Address", "")
            address = (
                refugee_point[first_index:last_index].replace("street", "")
                + ", Romania"
            )
            location = geolocator.geocode(address)
            if location is None:
                new_address = address.replace("RAdauti,", "")
                new_address = new_address.replace("County", "")
                location = geolocator.geocode(new_address)
            if location is None:
                reception_point.lon = ""
                reception_point.lat = ""
            else:
                reception_point.lon = str(location.longitude)
                reception_point.lat = str(location.latitude)
            reception_point.address = address
            reception_list.append(reception_point)

        return reception_list

    def decode_text_from_image(self) -> str:
        for file in os.scandir("temp"):
            try:
                image = Image.open(file.path)
            except:
                continue
            result_string = image_to_string(image)
            if result_string.find("Accommodation in Asylum") != -1:
                return result_string


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
        soup = BeautifulSoup(r.text, "html.parser")
        images = soup.findAll("img")
        self.folder_create(images)
        self.download_images(images, self._folder_name)
