# Scraper for Ukraine Centralized Information Guide

## Project Board [Here](https://github.com/orgs/Ukraine-Relief-Efforts/projects/1/views/6)



## Desired Information:

1. General guidelines
2. Reception points
3. Map link

We have some sample data exported in json below, but we now write our data to
DynamoDB.  Do not attempt to write json to the file system, which is mostly
read-only.

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


# Testing

We've got some basic integration tests put together for the scrapers.  They'll
scrape the real websites and do some sanity checks, but won't actually write to
dynamo.  You'll need tox:

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

These dependencies are stored on an AWS layer in production.  This shouldn't
matter to you, but someone ought to know :)

## Adding Dependencies

If you add a dependency, pop in in requirements.txt.  Make sure you run the
tests.  And try to run your stuff in AWS, too, which may not play quite as
nicely with some libraries as your local machine does.  Be mindful of the size
of your dependencies, as there are size limits of the combined code and layer
that hosts our dependencies.

# Testing with AWS

You'll want to zip up the entire project folder (but not the folder itself) and
upload that to a Lambda function, then hit the "Test" button.  You'll need to
get AWS access from someone on the Discord channel.

# Style

We (will) use Black to enforce a consistent style.  This will run in CI, and
will apparently be available as a Git hook (once the PR makes it in).
