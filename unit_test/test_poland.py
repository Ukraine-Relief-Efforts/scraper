# unit_tests/test_poland.py

import os
import sys
from unittest.mock import MagicMock, patch
import pytest
from bs4 import BeautifulSoup
import requests

# Import poland scraper
sys.path.insert(0, os.path.join("..", "src"))
from scrapers import poland


def test_get_reception_points_en():
    html = requests.get(poland.POLAND_PL_RECEPTION_URL)
    soup = BeautifulSoup(html.text)
    assert isinstance(poland.PolandScraper().get_reception_points_pl(soup), list)


def test_get_reception_points_pl():
    html = requests.get(poland.POLAND_PL_RECEPTION_URL)
    soup = BeautifulSoup(html.text)
    assert isinstance(poland.PolandScraper().get_reception_points_en(soup), list)


# def test_scrape():
#     assert poland.PolandScraper().scrape() is None

# From test_dynamo.py
# @pytest.fixture(autouse=True)
# def put_item():
#     """Mock dynamo.  Stupid dynamo."""
#     with patch("utils.dynamo.client.put_item", MagicMock(name="put_item")) as put_item:
#         yield put_item

# @pytest.fixture(autouse=True)
# def test_scrape_poland(put_item):
#     url = poland.POLAND_PL_URL
#     p = poland.PolandScraper().scrape_poland(url, "en", "")
#     assert isinstance(p, list)


# TODO:
# - Figure out dynmo write bypass for testing (still test methods)
# - Write tests for rest of poland.PolandScraper
# - Write tests for other country scrapers
