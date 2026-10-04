import logging
from typing import List, Dict, Any
import sys
import os
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class SapphireScraper(BaseScraper):
    """
    Scraper for Sapphire using HTML parsing (Demandware/SFRA).
    """
    def __init__(self):
        super().__init__(brand_name="Sapphire", base_url="https://pk.sapphireonline.pk")
        self.collections = [
            "/collections/ready-to-wear",
            "/collections/woman"
        ]

    def scrape(self) -> List[Dict[str, Any]]:
        logger.info(f"Starting HTML scrape for {self.brand_name}")
        products_data = []
        
        for collection in self.collections:
            url = f"{self.base_url}{collection}"
            try:
                self._delay()
                response = self.session.get(url, timeout=15)
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch {url}, status code {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                tiles = soup.find_all(class_='product-tile')
                
                for tile in tiles:
                    # Title
                    title_elem = tile.find(class_='pdp-link')
                    title = title_elem.text.strip() if title_elem else "Sapphire Dress"
                    
                    # URL
                    link_elem = tile.find('a', class_='link')
                    product_url = f"{self.base_url}{link_elem['href']}" if link_elem and link_elem.get('href') else url
                    
                    # Image
                    img_elem = tile.find('img', class_='tile-image')
                    image_url = ""
                    if img_elem:
                        image_url = img_elem.get('data-src') or img_elem.get('src', '')
                    
                    # Price
                    price = 0.0
                    original_price = None
                    
                    # Sale price usually in .sales .value
                    sale_elem = tile.select_one('.sales .value') or tile.select_one('.value.cc-price')
                    if sale_elem and sale_elem.get('content'):
                        try:
                            price = float(sale_elem.get('content'))
                        except ValueError:
                            pass
                            
                    # Original price usually in .strike-through .value or .list .value
                    orig_elem = tile.select_one('.strike-through .value') or tile.select_one('.list .value')
                    if orig_elem and orig_elem.get('content'):
                        try:
                            original_price = float(orig_elem.get('content'))
                        except ValueError:
                            pass
                            
                    if not price:
                        continue
                        
                    # Tags
                    subtitle = tile.find(class_='subtitle')
                    tags = subtitle.text.strip() if subtitle else collection.split('/')[-1]
                    
                    products_data.append({
                        "brand": self.brand_name,
                        "title": title,
                        "price": price,
                        "original_price": original_price, 
                        "availability": True,
                        "product_url": product_url,
                        "image_url": image_url,
                        "tags": tags
                    })
                    
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                
        logger.info(f"Successfully scraped {len(products_data)} products from {self.brand_name}")
        return products_data
