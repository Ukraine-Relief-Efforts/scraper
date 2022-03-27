"""Functionality related to geocoding."""
from pathlib import Path

import requests


def _get_key_path():
    return Path(__file__).parent / ".mapquest-key"


def address_to_coords(address):
    """Convert an address to latitude and longitude."""
    try:
        key = _get_key_path().read_text().strip()
    except FileNotFoundError:
        return None
    response = requests.get(
        "http://open.mapquestapi.com/geocoding/v1/address",
        params={"key": key, "location": address},
    )
    response.raise_for_status()
    data = response.json()
    lat_lng = data["results"][0]["locations"][0]["latLng"]
    return (lat_lng["lat"], lat_lng["lng"])
