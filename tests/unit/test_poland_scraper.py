import pytest
from scrapers.poland import PolandScraper
from unittest.mock import MagicMock


@pytest.fixture
def main_data():
    return """
    <html>
    <div class = "editor-content">
        <li>This is general info.</li>
    </div>
    </html>
    """


@pytest.fixture
def reception_data(build_kml):
    return """
    <div class="editor-content">
        <a href="https://www.google.pl/maps/place/Medyka+285,+37-732+Medyka/@77.7,77.7,17z/data=!3m1!4b1!4m5!3m4!1s0x473b7a1b8d10b8ef:0xfefb13192f90c961!8m2!3d42.1!4d42.2">MyName</a>
    </div>
    """


@pytest.fixture
def web_data(mrget, main_data, reception_data):
    def side_effect(url, headers):
        result = MagicMock(name="web_data")
        if "ukraina2" in url:
            result.content = main_data
        else:
            result.content = reception_data
        return result

    mrget.side_effect = side_effect


def test_scrape(mrget, unwrap_item, web_data):
    scraper = PolandScraper()
    scraper.scrape()
    result = unwrap_item()
    assert result
    print(result)
    assert result["country"] == "poland-pl"
    assert result["general"] == ["This is general info."]
    assert result["source"]

    assert result["reception"]
    assert len(result["reception"]) == 1
    reception = result["reception"][0]
    assert reception.name == "MyName"
    assert reception.address == "MyName"
    assert not reception.qr == "MyName"
    assert reception.lat == "42.1"
    assert reception.lon == "42.2"

    assert result["isoFormat"]
    assert result["dateTime"]
