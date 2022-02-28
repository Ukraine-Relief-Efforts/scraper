from dataclasses import dataclass


@dataclass
class Reception:
    name: str = ""
    address: str = ""
    qr: str = ""
    lat: str = ""
    lon: str = ""

    def __str__(self):
        return self.name
