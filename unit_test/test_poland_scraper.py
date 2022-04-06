from unittest.mock import MagicMock

import pytest

from scrapers.poland import PolandScraper


@pytest.fixture
def web_data(mrget):
    mrget().content = """
    <html>

    <h2>Some random locale heading</h2>

    <div class="editor-content">

        <div class="alert alert-info" role="alert">
            <p>General decoy</p>
        </div>

        <h3>Information for refugees from Ukraine</h3>

        <div class="alert alert-info" role="alert">
            <p>1. First.</p>
            <p>2. Second.</p>
            <p>3. Third:</p>
            <ul>
                <li>fourth,</li>
                <li>fifth,</li>
                <li>sixth.</li>
            </ul>
        </div>

        <div style="background:#eeeeee; border:1px solid #cccccc; padding:5px 10px">
            <strong>BORDER CROSSING POINT |&nbsp;RECEPTION POINT ADDRESS</strong>
        </div>

        <ul>
            <li><strong>Dorohusk-Jagodzin</strong></li>
        </ul>

        <p>
            Suchodolski Palace Communal Culture and Tourism Center, ul. Parkowa 5, 22-175 Dorohusk - housing estate
        </p>

        <div class="alert alert-info" role="alert">
            <p>
                I am bad.
            </p>
        </div>

    </div>
    </html>
    """


def test_scrape(mrget, unwrap_item, web_data):
    scraper = PolandScraper()
    scraper.scrape(locale="en")
    result = unwrap_item()
    assert result
    assert result["country"] == "poland-en"
    general = result["general"]
    assert len(general) == 6
    assert general == [
        "First.",
        "Second.",
        "Third:",
        "fourth,",
        "fifth,",
        "sixth.",
    ]
    assert result["source"]

    assert result["reception"]
    assert len(result["reception"]) == 1
    reception = result["reception"][0]
    assert (
        reception.name
        == "Suchodolski Palace Communal Culture and Tourism Center, ul. Parkowa 5, 22-175 Dorohusk - housing estate"
    )
    assert (
        reception.address
        == "Suchodolski Palace Communal Culture and Tourism Center, ul. Parkowa 5, 22-175 Dorohusk - housing estate"
    )
    assert not reception.qr

    # I haven't mocked the geocoding
    assert reception.lat is None
    assert reception.lon is None

    assert result["isoFormat"]
    assert result["dateTime"]
