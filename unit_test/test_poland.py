# unit_tests/test_poland.py

import os
import sys
from unittest.mock import MagicMock, patch
import pytest
from bs4 import BeautifulSoup
import requests

# Import poland scraper
sys.path.insert(0, os.path.join("..", "src"))
from scrapers.poland import PolandScraper, POLAND_PL_RECEPTION_URL, POLAND_PL_URL

html = requests.get(POLAND_PL_RECEPTION_URL)
soup = BeautifulSoup(html.text, features="html.parser")


@pytest.fixture
def pls():
    pls = PolandScraper()
    return pls


@pytest.fixture
def html_soup():
    html = requests.get(POLAND_PL_RECEPTION_URL)
    soup = BeautifulSoup(html.text)  # , features="html.parser")
    return html, soup


@pytest.fixture(params=["pl", "en"])
def test_get_core(pls, request):
    content = html.text
    text_arr = pls.get_core(content, request.param)
    assert isinstance(text_arr, list)


def test_get_reception_points_en(pls, html_soup):
    assert isinstance(pls.get_reception_points_pl(soup), list)


def test_get_reception_points_pl(pls):
    assert isinstance(pls.get_reception_points_en(soup), list)


def test_scrape(pls):
    assert pls.scrape() is None


def test_scrape_poland_pl():
    pass


@pytest.fixture(params=["pl", "en", "ua"])
def test_scrape_poland(pls, request):
    pass


# TODO:
# - Figure out dynmo write bypass for testing (still test methods)
# - Write tests for rest of PolandScraper
# - Write tests for other country scrapers
