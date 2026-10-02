import sys
import os
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# Add path so python can find the folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_setup import get_db
from database.models import Product
from backend.schemas import SearchResponse

app = FastAPI(title="Dress Scraper API")

# Allow frontend to connect without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Dress Scraper API. Go to /docs to test the API endpoints."}

@app.get("/search", response_model=SearchResponse)
def search_products(
    q: Optional[str] = Query(None, description="Search query like 'embroidered suit'"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum budget"),
    brand: Optional[str] = Query(None, description="Filter by brand (e.g. Alkaram Studio, Nishat Linen)"),
    on_sale: Optional[bool] = Query(None, description="Show only items on sale"),
    sort: Optional[str] = Query("price_asc", description="Sort by: price_asc, price_desc"),
    db: Session = Depends(get_db)
):
    """
    Search and filter products from the database based on user's budget and requirements.
    """
    # Start with all available products
    query = db.query(Product).filter(Product.availability == True)
    
    # 1. Search Query Filter (Title or Tags)
    if q:
        search_term = f"%{q}%"
        query = query.filter((Product.title.ilike(search_term)) | (Product.tags.ilike(search_term)))
        
    # 2. Budget / Price Filters
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
        
    # 3. Brand Filter
    if brand:
        query = query.filter(Product.brand.ilike(brand))
        
    # 4. Sale Filter
    if on_sale is True:
        query = query.filter(Product.is_on_sale == True)
        
    # 5. Sorting
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
        
    # Get results (limit to 100 for performance on UI)
    results = query.limit(100).all()
    
    return {
        "total_results": len(results),
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    # This block allows us to run the server via `python backend/main.py`
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
