# Scraper for Ukraine Centralized Information Guide

Desired Information:
1. General guidelines
2. Reception points
3. Map link

Data exported in json
Format (TBC):
* Poland:
```json
{
    "general": [ "str1", "str2"],
    "reception": [ 
          {
               "qr": "image link"
               "address": "address",
          },
          ....
    ]
}
```

# Data Source

* Poland border crossing info:
    * https://www.gov.pl/web/udsc/ukraina-en
    * https://www.gov.pl/web/udsc/ukraina2

* Moldova border crossing info:
    * https://www.border.gov.md/index.php/informare
