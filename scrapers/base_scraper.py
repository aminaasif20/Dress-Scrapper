import time
import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import sys
import os

# Add the parent directory to sys.path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class BaseScraper(ABC):
    """
    Abstract Base Class for all scrapers (SOLID: Open/Closed Principle).
    Defines the contract for scraping. We can add new scrapers without changing this class.
    """
    def __init__(self, brand_name: str, base_url: str):
        self.brand_name = brand_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": Config.USER_AGENT})

    def _delay(self):
        """Respectful delay between requests to avoid overloading servers."""
        time.sleep(Config.REQUEST_DELAY)

    def fetch_json(self, url: str) -> Dict[str, Any]:
        """Utility to fetch JSON data."""
        self._delay()
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method to be implemented by child classes."""
        pass
