from pathlib import Path

from utils.geo import address_to_coords, _get_key_path

# https://www.geocod.io/docs/


def address_to_coords_without_key_returns_none(fs):
    result = address_to_coords("asdf")
    assert result is None


def test_address_to_coords(mrget, fs):
    key_path = _get_key_path()
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text("my-key")
    # There's more stuff in the result, but this is all we care about
    mrget().json.return_value = {
        "results": [
            {
                "location": {"lat": 4, "lng": 2},
            }
        ]
    }
    result = address_to_coords(
        "Suchodolski Palace Communal Culture and Tourism Center, ul. Parkowa 5, 22-175 Dorohusk - housing estate"
    )
    assert result == (4, 2)
