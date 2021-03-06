"""Unit tests for dynamo functionality."""

import pytest

from utils import dynamo
from utils.reception import Reception


def test_write_to_dynamo_calls_put_item(put_item, unwrap_item):
    dynamo.write_to_dynamo(
        country="Sto Lat",
        event="",
        general=["user@example.com"],
        reception=[
            Reception(
                name="Sam",
                address="Pseudopolis Yard",
                lat="1.42",
                lon="2.42",
                qr="MyQr",
            )
        ],
        source="Wherever",
    )
    assert put_item.called
    item = unwrap_item()
    assert item["country"] == "Sto Lat"
    assert item["source"] == "Wherever"
    assert item["general"] == ["user@example.com"]
    assert item["dateTime"]
    assert item["isoFormat"]
    assert len(item["reception"]) == 1

    reception = item["reception"][0]
    assert reception.name == "Sam"
    assert reception.address == "Pseudopolis Yard"
    assert reception.lat == "1.42"
    assert reception.lon == "2.42"
    assert reception.qr == "MyQr"


def test_write_to_dynamo_with_some_blank_data_calls_put_item(put_item, unwrap_item):
    dynamo.write_to_dynamo(
        country="Sto Lat",
        event="",
        general=[],
        reception=[Reception(name="", address="", lat="1.42", lon="2.42", qr="")],
        source="",
    )
    assert put_item.called
    item = unwrap_item()
    assert item["country"] == "Sto Lat"
    assert item["source"] == ""
    assert item["general"] == []
    assert item["dateTime"]
    assert item["isoFormat"]
    assert len(item["reception"]) == 1

    reception = item["reception"][0]
    assert reception.name == ""
    assert reception.address == ""
    assert reception.lat == "1.42"
    assert reception.lon == "2.42"
    assert reception.qr == ""


def test_write_to_dynamo_with_test_suffix_calls_put_item_with_suffix(
    put_item, unwrap_item
):
    dynamo.write_to_dynamo(
        country="Sto Lat",
        event={"testSuffix": " suffix"},
        general=[],
        reception=[],
        source="",
    )
    assert put_item.called
    item = unwrap_item()
    assert item["country"] == "Sto Lat suffix"


def test_write_to_dynamo_removes_empty_general_lines(put_item, unwrap_item):
    dynamo.write_to_dynamo(
        country="Sto Lat",
        event={"testSuffix": " suffix"},
        general=[" ", "   \n ", "info"],
        reception=[],
        source="",
    )
    assert put_item.called
    item = unwrap_item()
    assert item["general"] == ["info"]


def test_write_to_dynamo_removes_duplicate_lines(put_item, unwrap_item):
    dynamo.write_to_dynamo(
        country="Sto Lat",
        event={"testSuffix": " suffix"},
        general=["foo", "foo", "bar"],
        reception=[],
        source="",
    )
    assert put_item.called
    item = unwrap_item()
    general = item["general"]
    assert len(general) == 2
    assert "foo" in general
    assert "bar" in general


def test_write_to_dynamo_with_no_existing_object_does_not_raise(
    put_item, get_item, unwrap_item
):
    get_item.side_effect = KeyError
    dynamo.write_to_dynamo(
        country="Sto Lat", event="", general=[], reception=[], source=""
    )
    assert put_item.called


def test_write_to_dynamo_with_general_data_loss_will_raise(
    put_item, unwrap_item, get_item
):
    get_item.return_value = {
        "Item": {
            "country": {"S": "Sto Lat"},
            "source": {"S": "Wherever"},
            "general": {"L": [str(x) for x in range(10)]},
            "reception": {"L": []},
        }
    }

    with pytest.raises(dynamo.DataLossError):
        dynamo.write_to_dynamo(
            country="Sto Lat",
            event="",
            general=[],
            reception=[Reception(name="", address="", lat="1.42", lon="2.42", qr="")],
            source="",
        )
    assert not put_item.called


def test_write_to_dynamo_with_reception_data_loss_will_raise(
    put_item, unwrap_item, get_item
):
    get_item.return_value = {
        "Item": {
            "country": {"S": "Sto Lat"},
            "source": {"S": "Wherever"},
            "general": {"L": []},
            "reception": {
                "L": [
                    {
                        "M": {
                            "name": {"S": "Sam"},
                            "lat": {"S": "42.12"},
                            "lon": {"S": "42.34"},
                            "address": {"S": "123 Fake St"},
                            "qr": {"S": ""},
                        }
                    }
                    for _ in range(10)
                ]
            },
        }
    }

    with pytest.raises(dynamo.DataLossError):
        dynamo.write_to_dynamo(
            country="Sto Lat",
            event="",
            general=[],
            reception=[],
            source="",
        )

    assert not put_item.called
