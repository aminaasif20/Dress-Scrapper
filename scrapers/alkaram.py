import logging
from typing import List, Dict, Any
import sys
import os

# Ensure we can import from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.base_scraper import BaseScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlkaramScraper(BaseScraper):
    """
    Scraper for Alkaram Studio. 
    Follows Single Responsibility Principle (SRP) by only focusing on Alkaram data extraction.
    If Alkaram changes their site, only this class needs to be updated.
    """
    def __init__(self):
        # We start with the /products.json endpoint as it's a common Shopify pattern.
        super().__init__(brand_name="Alkaram Studio", base_url="https://www.alkaramstudio.com")
        self.products_json_url = f"{self.base_url}/products.json?limit=250"

    def scrape(self) -> List[Dict[str, Any]]:
        logger.info(f"Starting scrape for {self.brand_name}")
        products_data = []
        try:
            # Let's try fetching the Shopify products.json
            data = self.fetch_json(self.products_json_url)
            products = data.get("products", [])
            
            for prod in products:
                title = prod.get("title", "")
                handle = prod.get("handle", "")
                product_url = f"{self.base_url}/products/{handle}"
                tags = prod.get("tags", [])
                
                # Variants hold the pricing
                variants = prod.get("variants", [])
                if not variants:
                    continue
                
                main_variant = variants[0]
                price = main_variant.get("price")
                compare_at_price = main_variant.get("compare_at_price")
                available = main_variant.get("available", False)
                
                # Images
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

    def save_to_csv(self, data: List[Dict[str, Any]], filename: str):
        """Utility function to save initial data to CSV for verification."""
        if not data:
            logger.warning("No data to save.")
            return
            
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        import csv
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        logger.info(f"Data saved to {filename}")

if __name__ == "__main__":
    scraper = AlkaramScraper()
    data = scraper.scrape()
    scraper.save_to_csv(data, "data/alkaram_temp.csv")
