# unit_test/test_romania.py

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join("..", "src"))
sys.path.insert(1, os.path.join("..", "src", "utils"))

# Romania mispelled in module name, stay woke
from scrapers.romaina_ro import RomaniaScraper, ROMANIA_INFO_URL, ROMANIA_MAP_URL
from utils.utils import get_website_content


@pytest.fixture
def rom():
    r = RomaniaScraper()
    return r


@pytest.fixture
def content():
    content = get_website_content(ROMANIA_INFO_URL)
    return content


# @pytest.fixture()
# def write_to_dynamo():
#     """Mock dynamo write"""
#     with patch("scrapers.romaina_ro.RomaniaScraper.write_to_dynamo", MagicMock(name="write_to_dynamo")) as dynamo_write:  #
#         yield dynamo_write


@patch("scrapers.romaina_ro.RomaniaScraper.write_to_dynamo", True)
def test_scrape(rom, write_dynamo):
    assert rom.scrape(event={"testSuffix": "test_romania"}) is True


def test_get_general(rom, content):
    text_arr = rom.get_general(content)
    assert isinstance(text_arr, list)
    assert text_arr


@pytest.fixture(params=[ROMANIA_INFO_URL, ROMANIA_MAP_URL])
def test_get_reception_points(rom, request):
    ra = rom._get_reception_points(request.param)
    assert ra
    assert isinstance(ra, list)
