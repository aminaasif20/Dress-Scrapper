import sys
import os
import logging
from datetime import datetime

# Add path so python can find the folders
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.alkaram import AlkaramScraper
from scrapers.sapphire import SapphireScraper
from scrapers.nishat import NishatScraper
from scrapers.normalizer import normalize_product
from database.db_setup import SessionLocal
from database.models import Product, PriceHistory, ScrapeRun

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_all_scrapers():
    """
    Runs all scrapers, normalizes the data, and saves it to the SQL Server database.
    """
    scrapers = [AlkaramScraper(), SapphireScraper(), NishatScraper()]
    db = SessionLocal()
    
    for scraper in scrapers:
        brand = scraper.brand_name
        logger.info(f"--- Starting scrape for {brand} ---")
        
        # 1. Record the start of this scrape run in the database
        run_log = ScrapeRun(brand=brand, status="RUNNING")
        db.add(run_log)
        db.commit()
        db.refresh(run_log)
        
        try:
            # 2. Get raw data from the website
            raw_products = scraper.scrape()
            
            # 3. Process and insert/update in Database
            for raw_p in raw_products:
                norm_p = normalize_product(raw_p)
                
                # Check if this product already exists based on its URL
                db_prod = db.query(Product).filter(Product.product_url == norm_p["product_url"]).first()
                
                if db_prod:
                    # Product exists, just update price and availability
                    price_changed = db_prod.price != norm_p["price"]
                    
                    db_prod.price = norm_p["price"]
                    db_prod.original_price = norm_p["original_price"]
                    db_prod.is_on_sale = norm_p["is_on_sale"]
                    db_prod.availability = norm_p["availability"]
                    db_prod.title = norm_p["title"]
                    db_prod.image_url = norm_p["image_url"]
                    
                    # If price changed, record the new price in history
                    if price_changed:
                        history = PriceHistory(product_id=db_prod.id, price=norm_p["price"])
                        db.add(history)
                else:
                    # New product, add it completely
                    new_prod = Product(**norm_p)
                    db.add(new_prod)
                    db.flush() # Flush to get the new_prod.id
                    
                    # Add its initial price history
                    history = PriceHistory(product_id=new_prod.id, price=norm_p["price"])
                    db.add(history)
            
            # Save all changes for this brand to the DB
            db.commit()
            
            # 4. Mark the scrape run as successful
            run_log.status = "SUCCESS"
            run_log.products_found = len(raw_products)
            run_log.completed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"--- Completed {brand}: Saved {len(raw_products)} products to DB ---")
            
        except Exception as e:
            logger.error(f"Error processing {brand}: {e}")
            db.rollback() # Undo any half-done changes
            
            # Mark the scrape run as failed
            run_log.status = "FAILED"
            run_log.error_message = str(e)
            run_log.completed_at = datetime.utcnow()
            db.commit()

    db.close()
    logger.info("All scrapers finished!")

if __name__ == "__main__":
    run_all_scrapers()
