import pytest
from scrapers.moldova_ro import MoldovaScraper
from unittest.mock import MagicMock


@pytest.fixture
def main_data():
    return """
    <html>
    <div class = "col-lg-10 offset-lg-1">
        <p>This is general info.</p>
    </div>
    </html>
    """


@pytest.fixture
def reception_data(build_kml):
    # We have 2 because 1 breaks in the xml parser...
    return build_kml(
        [{"styleUrl": "myStyle", "name": "MyName", "Point": {"coordinates": "4, 2"}}]
        * 2,
        as_xml=True,
    )


@pytest.fixture
def web_data(mrget, main_data, reception_data):
    def side_effect(url, headers):
        result = MagicMock(name="web_data")
        if "border" in url:
            result.content = main_data
        else:
            result.content = reception_data
        return result

    mrget.side_effect = side_effect


def test_scrape(mrget, unwrap_item, web_data):
    scraper = MoldovaScraper()
    scraper.scrape()
    result = unwrap_item()
    assert result
    print(result)
    assert result["country"] == "moldova-ro"
    assert result["general"] == ["This is general info."]
    assert result["source"]

    assert result["reception"]
    assert len(result["reception"]) == 2
    reception = result["reception"][0]
    assert reception.name == "MyName"
    assert reception.address == "MyName"
    assert not reception.qr == "MyName"
    assert reception.lat == "2"
    assert reception.lon == "4"

    assert result["isoFormat"]
    assert result["dateTime"]
