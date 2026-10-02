from pydantic import BaseModel
from typing import Optional, List

class ProductResponse(BaseModel):
    id: int
    brand: str
    title: str
    price: float
    original_price: float
    is_on_sale: bool
    availability: bool
    product_url: str
    image_url: str
    
    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    total_results: int
    results: List[ProductResponse]
