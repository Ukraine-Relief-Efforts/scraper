# Scraper for Ukraine Centralized Information Guide

Desired Information:
1. General guidelines
2. Reception points
3. Map link

Data exported in json
Format (TBC):
* Poland:
```json
// JSON format.
{
    "general": [ "str1", "str2"],
    "reception": [ 
          {
               "qr": "image link",
               "gmaps": "gmaps link",
               "address": "address",
          },
          ....
    ]
}

// Example with real data.
{
  "general": [
    "Jeżeli uciekasz przed konfliktem zbrojnym na Ukrainie, zostaniesz wpuszczony do Polski.",
    "Jeżeli nie masz zapewnionego miejsca pobytu w Polsce, udaj się do najbliższego punktu recepcyjnego.",
    ...
  ],
  "reception": [
    {
      "qr": "https://www.qr-online.pl/bin/qr/8caf19812112ea544f35e994cd58573c.png",
      "gmaps": "https://www.google.pl/maps/place/Gminny+Ośrodek+Kultury+i+Turystyki/@51.1653246,23.8026394,17z/data=!3m1!4b1!4m5!3m4!1s0x4723890b09b9cd4d:0x5747c0a6dfbbb992!8m2!3d51.1653213!4d23.8048281",
      "address": "Pałac Suchodolskich Gminny Ośrodek Kultury i Turystyki, ul. Parkowa 5, 22-175 Dorohusk – osiedle ​"
    },
    ...
  ]
}

```

# Data Source

* Poland border crossing info:
    * https://www.gov.pl/web/udsc/ukraina-en
    * https://www.gov.pl/web/udsc/ukraina2

* Moldova border crossing info:
    * https://www.border.gov.md/index.php/informare
