"""Scraper base class"""

from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """An abstract base class for scrapers"""

    @abstractmethod
    def scrape(self):
        """The abstract method."""
        pass
