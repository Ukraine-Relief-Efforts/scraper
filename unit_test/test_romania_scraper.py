import pytest
from scrapers.romaina_ro import RomaniaScraper
from unittest.mock import MagicMock


@pytest.fixture
def main_data():
    return """
    <html>
    <div class = "mrow txtcontent">
        <p>This is general info.</p>
    </div>
    </html>
    """


@pytest.fixture
def reception_data():
    return """
    <div class="txtcontent">
        <table>
            <tr><th><td>Header</td></th></tr>
            <tr>
                <td><span>MyName</span></td>
                <td>Blah</td>
                <td>Blah</td>
                <td><a href="https://www.google.ro/maps/dir//42.1,42.2/?hl=ro"></a></td>
            </tr>
        </table>
    </div>
    """


@pytest.fixture
def web_data(mrget, main_data, reception_data):
    def side_effect(url, headers):
        result = MagicMock(name="web_data")
        if "main" in url:
            result.content = main_data
        else:
            result.content = reception_data
        return result

    mrget.side_effect = side_effect


def test_scrape(mrget, unwrap_item, web_data):
    scraper = RomaniaScraper()
    scraper.scrape()
    result = unwrap_item()
    assert result
    print(result)
    assert result["country"] == "romania-ro"
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
