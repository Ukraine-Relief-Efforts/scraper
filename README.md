# Scraper for Ukraine Centralized Information Guide

## Project Board [Here](https://github.com/orgs/Ukraine-Relief-Efforts/projects/1/views/6)



## Desired Information:

1. General guidelines
2. Reception points
3. Map link

We have some sample data exported in json below, but we now write our data to DynamoDB.
 Do not attempt to write json to the file system, which is mostly read-only.

Format (TBC):

```json
// JSON format.
{
    "general": [ "general info about the border crossing.", "Usually split by sentences (in theory)"],
    "reception": [
          {
               "qr": "image link",
               "lat": "53.034",
               "lon": "53.034",
               "address": "Some Address",
               "name": "Some Name"
          },
          ....
    ]
    "source": "https://source.of/the/data/that/we.used",
    "country": "country-langcode",
    "dateTime": "python datetime object",
    "isoFormat": "date of scraping in iso format"
}

// Example with real data.
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
        },
    ],
    "dateTime": "2022-03-08  20:16:09  ",
    "source": "https://www.gov.pl/web/udsc/ukraina2",
    "general": [
        "If you are fleeing the Russian military aggression against Ukraine, you will be admitted to Poland.",
        "If you do not have a place of stay in Poland, go to the nearest reception point.",
        "At the reception desk: you will receive more information about your stay in Poland, we will provide you with temporary accommodation in Poland, you will receive a hot meal, a drink, basic medical care and a place to rest.
 ]
}

```

# Data Source

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

# Testing

We've got some basic integration tests put together for the scrapers. They'll
 scrape the real websites and do some sanity checks, but won't actually write
 to dynamo. You'll need tox:

```sh
pip install tox
```

Then, from the project directory:

```sh
tox
```

# Dependency Management

Dependencies are tracked in requirements.txt.  If you want to install locally,
you can do:

```sh
pip install -r requirements.txt
```

These dependencies are stored on an AWS layer in production. This shouldn't
matter to you, but someone ought to know :)

## Adding Dependencies

If you add a dependency, pop in in requirements.txt. Make sure you run the
tests.  And try to run your stuff in AWS, too, which may not play quite as
nicely with some libraries as your local machine does. Be mindful of the size
of your dependencies, as there are size limits of the combined code and layer
that hosts our dependencies.

Kindly refer to [SETUP.md](SETUP.md) on how to setup a basic working python
 virtual environment to allow you to easily add deps to requirements.txt

# Testing with AWS

You'll want to zip up the entire project folder (but not the folder itself) and
upload that to a Lambda function, then hit the "Test" button. You'll need to
get AWS access from someone on the Discord channel.

# Style

We use black to set up a consistent style, Kindly refer to [SETUP.md](SETUP.md)
 on how to setup precommit hooks for the linter.
