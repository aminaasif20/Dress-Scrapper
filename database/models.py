from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=False)
    is_on_sale = Column(Boolean, default=False)
    availability = Column(Boolean, default=True)
    product_url = Column(String(1000), unique=True, nullable=False)
    image_url = Column(String(1000))
    tags = Column(String(500))  # For categories like "lawn", "chiffon", "3-piece"
    category = Column(String(100)) # Will be populated by categorizer
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship with price history
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="price_history")


class ScrapeRun(Base):
    __tablename__ = "scrape_runs"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), nullable=False)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    products_found = Column(Integer, default=0)
    status = Column(String(20), default="RUNNING") # RUNNING, SUCCESS, FAILED
    error_message = Column(String(1000), nullable=True)
