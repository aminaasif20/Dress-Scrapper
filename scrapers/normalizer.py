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

def clean_title(title: str) -> str:
    """
    Cleans up messy titles by removing SKU codes and standardizing formats.
    e.g., "PES2SCHMV629_999 3 Piece - Embroidered Jacquard Suit" 
       -> "3 Piece - Embroidered Jacquard Suit"
    """
    # Remove alphanumeric SKUs at the start (e.g. ABC123_45, or similar)
    cleaned = re.sub(r'^[A-Z0-9_]+\s+', '', title)
    return cleaned.strip()
    
def extract_category(title: str) -> str:
    """
    Smartly categorizes the dress type and fabric using text analysis.
    (This acts like a fast, free LLM extraction for fashion titles).
    """
    t = title.lower()
    
    # Extract pieces
    pieces = ""
    if "3 piece" in t or "3-piece" in t or "3pc" in t: pieces = "3-Piece "
    elif "2 piece" in t or "2-piece" in t or "2pc" in t: pieces = "2-Piece "
    elif "1 piece" in t or "1-piece" in t or "1pc" in t: pieces = "1-Piece "
    
    # Extract fabric
    fabric = ""
    if "jacquard" in t: fabric = "Jacquard"
    elif "lawn" in t: fabric = "Lawn"
    elif "khaddar" in t: fabric = "Khaddar"
    elif "chiffon" in t: fabric = "Chiffon"
    elif "silk" in t: fabric = "Silk"
    elif "cambric" in t: fabric = "Cambric"
    elif "cotton" in t: fabric = "Cotton"
    
    # Extract type
    type_ = ""
    if "unstitched" in t or "loose fabric" in t or "freedom" in t: type_ = "Unstitched"
    elif "ready to wear" in t or "pret" in t: type_ = "Pret"
    
    category = f"{pieces}{fabric} {type_}".strip()
    return category if category else "Uncategorized"

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

    raw_title = str(raw_product.get("title", "")).strip()
    clean_t = clean_title(raw_title)
    category = extract_category(clean_t)

    return {
        "brand": str(raw_product.get("brand", "Unknown")).strip(),
        "title": clean_t,
        "price": price,
        "original_price": original_price,
        "is_on_sale": is_on_sale,
        "availability": bool(raw_product.get("availability", False)),
        "product_url": str(raw_product.get("product_url", "")).strip(),
        "image_url": str(raw_product.get("image_url", "")).strip(),
        "tags": str(raw_product.get("tags", "")).lower(),
        "category": category
    }
