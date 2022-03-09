from utils.utils import gmaps_url_to_lat_lon


def test_gmaps_url_to_lat_lon_with_3d():
    result = gmaps_url_to_lat_lon(
        "https://www.google.pl/maps/place/Medyka+285,+37-732+Medyka/@49.8051923,22.929263,17z/data=!3m1!4b1!4m5!3m4!1s0x473b7a1b8d10b8ef:0xfefb13192f90c961!8m2!3d49.8051889!4d22.9314517"
    )
    assert result
    assert result[0] == "49.8051889"
    assert result[1] == "22.9314517"


def test_gmaps_url_to_lat_lon_with_slashes():
    result = gmaps_url_to_lat_lon(
        "https://www.google.ro/maps/dir//46.78513359,28.138904570000022/?hl=ro"
    )
    assert result
    assert result[0] == "46.78513359"
    assert result[1] == "28.138904570000022"
