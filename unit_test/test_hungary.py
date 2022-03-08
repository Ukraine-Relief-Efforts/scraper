# unit_tests/test_hungary.py

import os
import sys
from unittest.mock import MagicMock, patch
import pytest
from bs4 import BeautifulSoup
import requests

# Import hungary scraper
sys.path.insert(0, os.path.join("..", "src"))
sys.path.insert(1, os.path.join("..", "src", "utils"))

from scrapers.hungary_hu import HungaryScraper, HUNGARY_URL
from utils.dynamo import write_to_dynamo
from utils.utils import get_reception_points, get_website_content, normalize


@pytest.fixture
def hun():
    h = HungaryScraper()
    return h


@pytest.fixture
def content():
    content = get_website_content(HUNGARY_URL)
    return content


def test_scrape(hun):
    hun.scrape()


def test_get_general(hun, content):
    text_arr = hun._get_general(content)
    assert isinstance(text_arr, list)
    assert text_arr


def test_get_reception_points(hun):
    recep_pts = hun._get_reception_points()
    assert isinstance(recep_pts, list)
    assert recep_pts
