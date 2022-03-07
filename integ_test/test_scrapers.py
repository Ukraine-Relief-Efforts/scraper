from unittest.mock import MagicMock, patch

import pytest

import utils.dynamo
from scrapers.hungary_hu import HungaryScraper
from scrapers.moldova_ro import MoldovaScraper
from scrapers.poland import PolandScraper
from scrapers.romaina_ro import RomaniaScraper
from scrapers.slovakia_sk import SlovakiaScraper


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


@pytest.fixture()
def check_common(put_item):
    def func(country):
        assert put_item.called
        cargs = put_item.call_args
        assert cargs.kwargs["TableName"] == "TechForUkraine-CIG"
        item = cargs.kwargs["Item"]
        assert item
        assert item["country"]
        assert item["country"]["S"]
        assert item["country"]["S"] == country
        assert item["general"]
        assert item["source"]
        assert item["source"]["S"]
        assert item["reception"]
        assert item["reception"]["L"] is not None

        for reception in item["reception"]["L"]:
            assert set(reception.keys()) == {"M"}
            assert set(reception["M"]) == {"name", "lat", "lon", "address", "qr"}
            for value in reception["M"].values():
                assert set(value.keys()) == {"S"}

        general = [line["S"] for line in item["general"]["L"]]
        reception = [
            {
                "name": rec["M"]["name"]["S"],
                "lat": rec["M"]["lat"]["S"],
                "lon": rec["M"]["lon"]["S"],
                "address": rec["M"]["address"]["S"],
                "qr": rec["M"]["qr"]["S"],
            }
            for rec in item["reception"]["L"]
        ]

        for rec in reception:
            # Will raise if not a float
            _ = float(rec["lat"])
            _ = float(rec["lon"])
            assert rec["name"]

        names = {rec["name"] for rec in reception}
        addresses = {rec["address"] for rec in reception}

        # These are very low numbers, and if we're below this, something is
        # probably wrong
        assert len(general) > 5
        assert len(reception) > 5

        assert len(names) > 5
        # All these say 'WIP' right now
        # Or not? Think I fixed that
        assert len(addresses) > 5

        return item, general, reception

    return func


def test_scrape_poland_pl(check_common):
    poland_scraper = PolandScraper()
    poland_scraper.scrape_poland_pl()
    check_common("poland-pl")


def test_scrape_romania_ro(check_common):
    scraper = RomaniaScraper()
    scraper.scrape()
    check_common("romania-ro")

def test_scrape_slovakia_sk(check_common):
    scraper = SlovakiaScraper()
    scraper.scrape()
    check_common("slovakia-sk")

def test_scrape_hungary_hu(check_common):
    # This one's too big...just doing a spot check
    hungary_scraper = HungaryScraper()
    hungary_scraper.scrape()
    item, general, reception = check_common("hungary-hu")
    # This is just a check to make sure we were scraping a minimal amount of data that suggests the website didn't drastically change format
    assert len(general) >= 30

    # First
    assert "Határátlépéssel kapcsolatos általános információk" in general
    # Some...more stuff that looks important?
    assert "kotegyanhrk@bekes.police.hu" in general
    assert "+36-66-572-620" in general
    assert "biharkereszteshrk@hajdu.police.hu" in general
    assert "nyirabranyhrk@hajdu.police.hu" in general
    assert "+36-52-596-009" in general
    # Last
    assert "Letenye Autópálya" in general
    assert len(reception) == 58

    names = {rec["name"] for rec in reception}
    assert "Garbolc - Bercu" in names


def test_scrape_moldova_ro(check_common):
    moldova_scraper = MoldovaScraper()
    moldova_scraper.scrape()
    item, general, reception = check_common("moldova-ro")
    # I do not know what this means, but for the moment, we don't want it to
    # change significantly.
    assert general == [
        "TRAVERSAREA FRONTIEREI DE STAT MOLDO-UCRAINENE",
        "Pentru cetăţenii Republicii Moldova şi Ucrainei:",
        "Este necesar paşaportul sau buletinul de identitate (pentru locuitorii raioanelor de frontieră) în dependenţă şi în corespundere cu regulile stabilite prin «Acordul între Guvernul Republicii Moldova şi Guvernul Ucrainei cu privire la punctele de trecere la frontiera de stat moldo-ucraineană şi simplificarea formalităţilor la trecerea frontierei de către cetăţenii care locuiesc în raioanele de frontieră» semnat în or. Chişinău, pe data de 11 martie 1997.",
        "Lista raioanelor de frontieră ale Republicii Moldova, locuitorii cărora traversează frontiera de stat moldo-ucraineană în mod simplificat.",
        "Lista raioanelor de frontieră a Ucrainei, locuitorii cărora traversează frontiera de stat moldo-ucraineană în mod simplificat.",
        "Regiunea Cernăuţi :",
        "Regiunea Odesa:",
        "Mijloacele de transport traversează frontiera de stat a Republicii Moldova pe baza documentelor valabile, care permit trecerea frontierei de stat.",
        "Documentele valabile pentru mijloacele de transport, înregistrate pe teritoriul Republicii Moldova:",
        "a) permisul de conducere perfectat pe numele conducătorului auto, valabil pentru categoria (subcategoria) din care face parte autovehiculul condus; b) certificatul de înmatriculare a vehiculului; c) poliţa de asigurare obligatorie de răspundere civilă a deţinătorilor mijloacelor de transport auto; d) actele referitoare la natura şi masa încărcăturii, în cazurile stabilite de legislaţie.",
    ]

    names = {rec["name"] for rec in reception}
    assert "Medveja-Zelionaia" in names
    assert "Criva-Mamaliga" in names
    assert "Cahul-Oancea" in names
