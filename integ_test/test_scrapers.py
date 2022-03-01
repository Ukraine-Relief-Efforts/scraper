from unittest.mock import MagicMock, patch

import pytest

import utils.dynamo
from scrapers.hungary_hu import HungaryScraper
from scrapers.moldova_ro import MoldovaScraper
from scrapers.poland import PolandScraper


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
        return item, general, reception

    return func


# def test_poland_pl(put_item, check_common):
#     poland_scraper = PolandScraper()
#     poland_scraper.scrape_poland_pl()
#     check_common("poland-pl")


# def test_poland_en(put_item, check_common):
#     poland_scraper = PolandScraper()
#     poland_scraper.scrape_poland_en()
#     check_common("poland-en")


def test_poland_ua(put_item, check_common):
    poland_scraper = PolandScraper()
    poland_scraper.scrape_poland_ua()
    check_common("poland-ua")


def test_scrape_hungary_hu(put_item, check_common):
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

    assert reception[0] == {
        "name": "Letenye I. Közúti Határátkelőhely",
        "lat": "46.420334",
        "lon": "16.697088",
        "address": "",
        "qr": "",
    }
    assert reception[1] == {
        "name": "Letenye II. Autópálya Határátkelőhely",
        "lat": "46.41246",
        "lon": "16.70346",
        "address": "",
        "qr": "",
    }
    assert reception[2] == {
        "name": "Murakeresztúr Vasúti Határátkelőhely",
        "lat": "46.358938",
        "lon": "16.85126",
        "address": "",
        "qr": "",
    }
    assert reception[-1] == {
        "name": "Garbolc - Bercu",
        "lat": "47.9448241",
        "lon": "22.8628",
        "address": "",
        "qr": "",
    }


# FIXME: This is broken, looks like the ordering is different than expected, I'm getting address first and name last
def test_scrape_moldova_ro(put_item, check_common):
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
    # TODO: Don't test hundreds of lines of crap after we've finished the kml
    # migration
    assert reception == [
        {
            "address": "",
            "lat": "48.1286973",
            "lon": "28.4190675",
            "name": "Vasilcău-Velikaia Koșnița",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.1631563",
            "lon": "28.3114161",
            "name": "Soroca-Țekinovca",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.1432364",
            "lon": "28.3041343",
            "name": "Soroca-Țekinovka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.8646064",
            "lon": "28.2180899",
            "name": "Mărculești Aeroport Internațional",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.237407",
            "lon": "28.2980678",
            "name": "Cosăuți-Iampol",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.227819",
            "lon": "28.2793194",
            "name": "Cosăuți-Iampol",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.4428872",
            "lon": "27.7868838",
            "name": "Otaci-Moghileov-Podolsk",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.3986264",
            "lon": "27.8756567",
            "name": "Unguri-Bronița",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.4430894",
            "lon": "27.7844218",
            "name": "Vălcineț-Moghileov-Podolsk",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.4384185",
            "lon": "27.4629002",
            "name": "Ocnița-Sokireani",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.4359842",
            "lon": "27.4620966",
            "name": "Ocnița-Sokireanî",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.4332768",
            "lon": "27.3767242",
            "name": "Clocușna-Sokireanî",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.3754359",
            "lon": "27.0488263",
            "name": "Briceni-Rossoșanî",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.3950352",
            "lon": "27.1049958",
            "name": "Grimăncăuți-Vașkivțî",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.4160991",
            "lon": "26.8267407",
            "name": "Larga-Kelmențî",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.3575029",
            "lon": "26.7622687",
            "name": "Medveja-Zelionaia",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.4277221",
            "lon": "27.0652115",
            "name": "Larga-Kelmențî",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.3518679",
            "lon": "26.7934087",
            "name": "Medveja-Zelionaia",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.2652082",
            "lon": "26.6255316",
            "name": "Criva-Mamaliga",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.2542634",
            "lon": "26.8015744",
            "name": "Lipcani-Rădăuți-Prut",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.8404434",
            "lon": "27.2274752",
            "name": "Costești-Stînca",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.8460281",
            "lon": "27.7774729",
            "name": "Bălți Aeroport Internațional",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.3202968",
            "lon": "27.6102466",
            "name": "Sculeni-Scuelni",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.2096047",
            "lon": "27.7881118",
            "name": "Ungheni-Iași",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.794229",
            "lon": "28.1618137",
            "name": "Leușeni-Albița",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.9168681",
            "lon": "28.1220363",
            "name": "Cahul-Oancea",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.4716336",
            "lon": "28.1986358",
            "name": "Giurgiulești-Reni",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.4731043",
            "lon": "28.1982677",
            "name": "Giurgiulești-Galați",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.470935",
            "lon": "28.2031415",
            "name": "Giurgiulești-Port",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.4758141",
            "lon": "28.2069202",
            "name": "Giurgiulești-Reni",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.5399583",
            "lon": "28.3454981",
            "name": "Cișmichioi-Dolinscoe",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.528986",
            "lon": "28.4203324",
            "name": "Etulia-Fricăței",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.6976875",
            "lon": "28.498158",
            "name": "Vulcănești-Vinogradovka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.7675332",
            "lon": "28.6187404",
            "name": "Cairaclia-Zaliznicinoe",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.9830203",
            "lon": "28.8444251",
            "name": "Ceadîr-Lunga - Novîe-Troianî",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.079207",
            "lon": "28.966093",
            "name": "Ceadîr-Lunga - Maloiaroslaveț",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.324282",
            "lon": "28.9883993",
            "name": "Basarabeasca-Serpniovo",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.844174",
            "lon": "28.263148",
            "name": "Aeroportul Internațional Cahul",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.5037478",
            "lon": "29.0399966",
            "name": "Troițcoe-Visoceanskoe",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.4712872",
            "lon": "29.3989602",
            "name": "Săiți-Lesnoe",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.413607",
            "lon": "30.1607361",
            "name": "Palanca - Maiki-Udobnoe",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.3865733",
            "lon": "30.0887191",
            "name": "Tudora-Starokazacie",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.3707702",
            "lon": "29.8436202",
            "name": "Caplani-Crutoiarovca",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.4594727",
            "lon": "28.9670505",
            "name": "Iserlia-Petrovka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.3544235",
            "lon": "29.6150709",
            "name": "Volontir-Faraonovka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.8914807",
            "lon": "28.7613885",
            "name": "Copceac-Alexandrovka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.444573",
            "lon": "29.3054686",
            "name": "Ucrainca-Lesnoe",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.1769039",
            "lon": "27.2956181",
            "name": "Direcţia regională NORD",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.197557",
            "lon": "27.7887154",
            "name": "Direcția regionala Vest",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.1977465",
            "lon": "27.7889085",
            "name": "Centrul de Excelență în Securitatea Frontierei",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.045417",
            "lon": "28.8298523",
            "name": "Inspectoratul General al Poliției de Frontieră",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.9354074",
            "lon": "28.9356709",
            "name": "Aeroportul Internațional Chișinău",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.9063749",
            "lon": "28.1899738",
            "name": "Direcția regională Sud",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.5168232",
            "lon": "29.6579361",
            "name": "Direcția regională Est",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.7981987",
            "lon": "29.219579",
            "name": "Cobasna-Slobodka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.7365004",
            "lon": "29.9640239",
            "name": "Novosaviţcaia-Kuciurgan",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.1335269",
            "lon": "28.7393052",
            "name": "Hristovaia-Bolgan",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.4036996",
            "lon": "29.3290972",
            "name": "Goianul Nou-Platonovo",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.7360761",
            "lon": "29.9782355",
            "name": "Pervomaisc-Kuciurgan",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.1272942",
            "lon": "28.4992733",
            "name": "Hruşca-Velikaia Kosniţa",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.8794374",
            "lon": "29.2727495",
            "name": "Broşteni-Timkovo",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.9626059",
            "lon": "28.9957841",
            "name": "Vadul Turcului-Şerşenţî",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.7046992",
            "lon": "29.2167076",
            "name": "Vărăncău-Stanislavka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.3447818",
            "lon": "29.5800375",
            "name": "Colosova-Iosipovka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.9233343",
            "lon": "29.6827473",
            "name": "Blijnii Hutor-Slaveanoserbka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.5857238",
            "lon": "29.9513078",
            "name": "Nezavertailovca-Gradinţî",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.0211052",
            "lon": "28.8608169",
            "name": "Valea Adîncă-Zagnitkovo",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.8022608",
            "lon": "29.2153252",
            "name": "Cobasna-Domniţa",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.458269",
            "lon": "29.1908568",
            "name": "Ţîbuleuca-Ţehanovka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.4336892",
            "lon": "29.2707431",
            "name": "Dubău-Dubovo",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.2503971",
            "lon": "29.5521283",
            "name": "Mociarovca-Pavlovka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.8633143",
            "lon": "29.7473824",
            "name": "Tiraspol-Grebeniki",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.8334792",
            "lon": "29.8947504",
            "name": "Frunză-Rozalovka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.1541551",
            "lon": "28.6347156",
            "name": "Ocniţa-Grabarivka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.9581434",
            "lon": "29.5568348",
            "name": "Mălăieşti-Velikopolskoe",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.108809",
            "lon": "28.853669",
            "name": "Rotari-Studeonoe",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.5269221",
            "lon": "29.1377755",
            "name": "Jura-Fedoseevka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.9554918",
            "lon": "29.1867431",
            "name": "Plopi-Crutîe",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.9782057",
            "lon": "28.959658",
            "name": "Vadul Turcului-Alexeevka",
            "qr": "",
        },
        {
            "address": "",
            "lat": "47.0447627",
            "lon": "28.8283074",
            "name": "Direcția regională Centru",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.7365967",
            "lon": "28.581513",
            "name": "Mirnoe-Tabaki",
            "qr": "",
        },
        {
            "address": "",
            "lat": "48.2633119",
            "lon": "26.6273397",
            "name": "PTF Criva - Mamaliga",
            "qr": "",
        },
        {
            "address": "",
            "lat": "46.3187046",
            "lon": "28.9754094",
            "name": "Basarabeasca - Serpniovo-1",
            "qr": "",
        },
        {
            "address": "",
            "lat": "45.817684",
            "lon": "28.6972739",
            "name": "Copciac-Cervonoarmeiskoe",
            "qr": "",
        },
    ]
