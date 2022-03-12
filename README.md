# Scraper for Ukraine Centralized Information Guide [Project Board](https://github.com/orgs/Ukraine-Relief-Efforts/projects/1/views/6)

## Desired Information:

1. General guidelines
2. Reception points
3. Map link

We have some sample data exported in json below, but we now write our data to DynamoDB.
Do not attempt to write json to the file system, which is mostly read-only.

Format (TBC):

```json
{
  "general": [
    "general info about the border crossing.",
    "Usually split by sentences (in theory)"
  ],
  "reception": [
    {
      "qr": "image link",
      "lat": "53.034",
      "lon": "53.034",
      "address": "Some Address",
      "name": "Some Name"
    }
  ]
  "source": "https://source.of/the/data/that/we.used",
  "country": "country-langcode",
  "dateTime": "python datetime object",
  "isoFormat": "date of scraping in iso format"
}
```
```json
{
  "country": "poland-en",
  "isoFormat": "2022-03-08T20:16:09.430882",
  "reception": [
    {
      "name": "Suchodolski Palace Communal Culture and Tourism Center, ul. Parkowa 5, 22-175 Dorohusk - housing estate",
      "qr": "",
      "lon": "23.8048281",
      "address": "Suchodolski Palace Communal Culture and Tourism Center, ul. Parkowa 5, 22-175 Dorohusk - housing estate",
      "lat": "51.1653213"
    }
  ],
  "dateTime": "2022-03-08  20:16:09  ",
  "source": "https://www.gov.pl/web/udsc/ukraina2",
  "general": [
    "If you are fleeing the Russian military aggression against Ukraine, you will be admitted to Poland.",
    "If you do not have a place of stay in Poland, go to the nearest reception point.",
    "At the reception desk: you will receive more information about your stay in Poland, we will provide you with temporary accommodation in Poland, you will receive a hot meal, a drink, basic medical care and a place to rest."
  ]
}
```

# Sources

* Poland border crossing info:
    * https://www.gov.pl/web/udsc/ukraina-en
    * https://www.gov.pl/web/udsc/ukraina2
    * https://www.gov.pl/web/udsc/punkty-recepcyjne2

* Moldova border crossing info:
    * https://www.border.gov.md/ro/ucraina
    * http://www.google.com/maps/d/kml?forcekml=1&mid=1S38hHlp67u7UoFgVGFC-GCU2Efsn6WeC

* Hungary border crossing info:
    * https://www.police.hu/hu/hirek-es-informaciok/hatarinfo/hataratlepessel-kapcsolatos-informaciok
    * http://www.google.com/maps/d/kml?forcekml=1&mid=1d54nWG4ig0rmBPj3K3RF3I1mkY0KOFZd

* Romania border crossing info:
    * https://www.politiadefrontiera.ro/ro/main/pg-conditii-generale-de-calatorie-a-cetatenilor-din-statele-care-nu-sunt-membre-ale-uniunii-europene-si-spatiului-economic-european-147.html
    * https://www.politiadefrontiera.ro/ro/traficonline/?dt=1&vw=2
