from collections import defaultdict
from PIL import Image
from pytesseract import image_to_string

from scrapers.base_scraper import BaseScraper
from utils.dynamo import write_to_dynamo
from utils.reception import Reception


class RomaniaScraper(BaseScraper):
    def __init__(self):
        self.mapping = defaultdict(Reception)
        self.mapping["Halmeu"] = Reception("Halmeu", "Halmeu", "", "47.99949245007817", "23.001865588674413")
        self.mapping["Sighetu Marmatiei"] = Reception("Sighetu Marmatiei", "Sighetu Marmatiei", "", "47.9389198",
                                                      "23.8775945")
        self.mapping["Siret"] = Reception("Siret", "Siret", "", "47.987979983510925", "26.061198978070973")
        self.mapping["Isaccea"] = Reception("Isaccea", "Siret", "", "45.28398915528812", "28.453329592029377")

    def scrape(self):
        text = self.decode_text_from_image()
        border_crossings = self.find_border_crossings(text)
        reception_list = list()
        for border in border_crossings:
            reception_list.append(self.mapping[border])
        write_to_dynamo("Romania", "Border crossing pointsś", reception_list, "")

    def decode_text_from_image(self) -> str:
        image = Image.open("data/romanian_data.png")
        result_string = image_to_string(image)
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
