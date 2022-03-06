import pytest
import os
import sys

sys.path.insert(0, os.path.join("..", "src"))

from scrapers import base_scraper
from scrapers import poland



def test_poland_get_core():
    p = poland.PolandScraper()
    assert isinstance(p.get_core(content="<h1></h1>", locale='en'), list)

