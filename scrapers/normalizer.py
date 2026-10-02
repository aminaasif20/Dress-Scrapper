import re
from typing import Dict, Any

def normalize_price(price_val: Any) -> float:
    """
    Converts price string or number to a clean float.
    Handles 'Rs. 5,000', '5000', '5000.00' etc.
    """
    if price_val is None:
        return 0.0
        
    if isinstance(price_val, (int, float)):
        return float(price_val)
        
    # Convert string
    price_str = str(price_val)
    # Remove everything except digits and decimal point
    clean_str = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(clean_str)
    except ValueError:
        return 0.0

def normalize_product(raw_product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes a raw product dictionary and normalizes its fields into a standard schema.
    """
    price = normalize_price(raw_product.get("price"))
    original_price = normalize_price(raw_product.get("original_price"))
    
    # If no original price is given, or if it's less than current price, set it to current price
    if original_price <= 0 or original_price < price:
        original_price = price
        
    is_on_sale = original_price > price

    return {
        "brand": str(raw_product.get("brand", "Unknown")).strip(),
        "title": str(raw_product.get("title", "")).strip(),
        "price": price,
        "original_price": original_price,
        "is_on_sale": is_on_sale,
        "availability": bool(raw_product.get("availability", False)),
        "product_url": str(raw_product.get("product_url", "")).strip(),
        "image_url": str(raw_product.get("image_url", "")).strip(),
        "tags": str(raw_product.get("tags", "")).lower()
    }
