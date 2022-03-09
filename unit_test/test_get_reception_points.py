from utils.utils import get_reception_points


def test_get_reception_points_returns_reception_points(build_kml):
    result = get_reception_points(
        kml=build_kml(
            [{"styleUrl": "myStyle", "name": "Steve", "Point": {"coordinates": "4, 2"}}]
        )
    )
    assert result
    assert len(result) == 1
    place = result[0]
    assert place.name == "Steve"
    assert place.address == place.name  # This is supposedly temporary
    assert place.lon == "4"
    assert place.lat == "2"
