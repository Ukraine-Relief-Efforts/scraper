from unittest.mock import MagicMock, patch

import pytest
import requests
import xmltodict
from pyfakefs import fake_filesystem_unittest

from utils import dynamo
from utils.reception import Reception


@pytest.fixture(autouse=True)
def build_kml():
    def func(places, folder_name="Places", as_xml=False):
        result = {
            "kml": {
                "Document": {
                    "Folder": [
                        {"name": "Decoy"},
                        {"name": folder_name, "Placemark": places},
                    ]
                }
            }
        }
        if as_xml:
            return xmltodict.unparse(result)
        return result

    return func


@pytest.fixture(autouse=True)
def put_item():
    """Mock dynamo.  Stupid dynamo."""
    with patch("utils.dynamo.client.put_item", MagicMock(name="put_item")) as put_item:
        yield put_item


@pytest.fixture(autouse=True)
def get_item():
    """Mock dynamo.... AGAIN!??!!?! What is this garbo..."""
    with patch("utils.dynamo.client.get_item", MagicMock(name="get_item")) as get_item:
        yield get_item


@pytest.fixture(autouse=True)
def mrget():
    with patch("requests.get", MagicMock(name="requests_get")) as result:
        yield result


@pytest.fixture(autouse=True)
def mrpost():
    with patch("requests.post", MagicMock(name="requests_post")) as result:
        yield result


@pytest.fixture
def unwrap_item(put_item):
    def func():
        cargs = put_item.call_args
        assert cargs.kwargs["TableName"] == "TechForUkraine-CIG"
        item = cargs.kwargs["Item"]
        assert item
        return {
            "country": item.get("country", {}).get("S"),
            "general": [gen["S"] for gen in item["general"]["L"]],
            "source": item.get("source", {}).get("S"),
            "reception": [
                Reception(
                    name=rec["M"]["name"]["S"],
                    lat=rec["M"]["lat"]["S"],
                    lon=rec["M"]["lon"]["S"],
                    qr=rec["M"]["qr"]["S"],
                    address=rec["M"]["address"]["S"],
                )
                for rec in item.get("reception", {}).get("L")
            ],
            "isoFormat": item["isoFormat"]["S"],
            "dateTime": item["dateTime"]["S"],
        }

    return func
