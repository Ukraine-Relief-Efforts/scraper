# unit_test/test_moldova.py

import os
import sys


import os
import sys
from unittest.mock import MagicMock, patch
import pytest
from bs4 import BeautifulSoup
import requests
import xmltodict

# Import hungary scraper
sys.path.insert(0, os.path.join("..", "src"))
sys.path.insert(1, os.path.join("..", "src", "utils"))

from scrapers.moldova_ro import MoldovaScraper, MOLDOVA_UKRAINE_URL, MOLDOVA_KML
from utils.dynamo import write_to_dynamo
from utils.constants import HEADERS
from utils.utils import get_reception_points, get_website_content


@pytest.fixture
def mol():
    m = MoldovaScraper()
    return m


@pytest.fixture
def content():
    content = get_website_content(MOLDOVA_UKRAINE_URL)
    return content


def test_scrape(mol):
    assert mol.scrape() is None


def test_get_general(mol, content):
    text_arr = mol.get_general(content)
    assert isinstance(text_arr, list)
    assert text_arr


def test_get_reception_points(mol):
    kml_str = requests.get(MOLDOVA_KML, headers=HEADERS).content
    kml = xmltodict.parse(kml_str, dict_constructor=dict)
    rp = get_reception_points(kml)
    assert mol._get_reception_points() == rp
