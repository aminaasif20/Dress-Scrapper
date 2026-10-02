import logging
from typing import List, Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class SapphireScraper(BaseScraper):
    """
    Scraper for Sapphire.
    """
    def __init__(self):
        super().__init__(brand_name="Sapphire", base_url="https://pk.sapphireonline.pk")
        self.products_json_url = f"{self.base_url}/products.json?limit=250"

    def scrape(self) -> List[Dict[str, Any]]:
        logger.info(f"Starting scrape for {self.brand_name}")
        products_data = []
        try:
            data = self.fetch_json(self.products_json_url)
            products = data.get("products", [])
            
            for prod in products:
                title = prod.get("title", "")
                handle = prod.get("handle", "")
                product_url = f"{self.base_url}/products/{handle}"
                tags = prod.get("tags", [])
                
                variants = prod.get("variants", [])
                if not variants:
                    continue
                
                main_variant = variants[0]
                price = main_variant.get("price")
                compare_at_price = main_variant.get("compare_at_price")
                available = main_variant.get("available", False)
                
                images = prod.get("images", [])
                image_url = images[0].get("src") if images else ""

                products_data.append({
                    "brand": self.brand_name,
                    "title": title,
                    "price": price,
                    "original_price": compare_at_price,
                    "availability": available,
                    "product_url": product_url,
                    "image_url": image_url,
                    "tags": ", ".join(tags)
                })
            
            logger.info(f"Successfully scraped {len(products_data)} products from {self.brand_name}")
            return products_data
        
        except Exception as e:
            logger.error(f"Failed to scrape {self.brand_name}: {e}")
            return []
