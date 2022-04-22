import logging
import re

from scrapers.base_scraper import BaseScraper
from utils.dynamo import write_to_dynamo
from utils.geo import address_to_coords
from utils.reception import Reception
from utils.utils import get_website_content, gmaps_url_to_lat_lon, normalize

POLAND_URL = "https://www.gov.pl/web/family/information-for-refugees-from-ukraine"

# We use the content of header tags (h2, h3) to check the locale
LOCALE_MAPPING = {
    "en": "Information for refugees from Ukraine",
    "ua": "Інформація для біженців з України",
    "ru": "Информация для беженцев из Украины",
}


class LocaleNotFound(Exception):
    """Error for a locale not found on the page."""


class PolandScraper(BaseScraper):
    def scrape(self, event="", locale="en"):
        content = get_website_content(POLAND_URL)

        general, rec_strings = self._extract_general_and_reception_strings(
            content=content, locale=locale
        )

        reception_points = [self._reception_from_str(s) for s in rec_strings]

        country = "poland-" + locale
        write_to_dynamo(country, event, general, reception_points, POLAND_URL)

    def _extract_general_and_reception_strings(self, content, locale):
        alerts = content.select("div.alert.alert-info")
        general = []
        reception_strings = []

        for alert in alerts:
            # Determine if we're looking at the right section for our locale
            heading = alert.find_previous(["h2", "h3"])
            heading_text = heading.string
            if LOCALE_MAPPING[locale] != heading_text:
                # Nope, keep searching
                continue

            # First - find general info
            for tag in alert.find_all(["p", "li"]):
                text = tag.string
                # They format some paragraphs like numbered lists now for some
                # reason, so remove that junk
                text = re.sub(r"^\d+\.\s*", "", text).strip()
                general.append(text)

            # Now look for reception points
            for tag in alert.find_next_siblings():
                class_ = tag.get("class")
                if class_:
                    if "alert" in class_:
                        break
                if tag.name == "p":
                    reception_strings.append(tag.string.strip())
            # We only need to do the one locale, so quit
            break
        else:
            raise LocaleNotFound(locale)

        return (general, reception_strings)

    def _reception_from_str(self, value):
        result = Reception()
        result.address = result.name = value.strip()
        coords = address_to_coords(result.address)
        if coords:
            result.lat = str(coords[0])
            result.lon = str(coords[1])
        else:
            result.lat = result.lon = None

        return result
