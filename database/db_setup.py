import sys
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from database.models import Base

logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine
try:
    engine = create_engine(Config.DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Error connecting to SQL Server: {e}")
    engine = None
    SessionLocal = None

def init_db():
    """
    Creates all tables in the SQL Server database if they don't exist.
    """
    if engine is None:
        logger.error("Database engine is not initialized. Check connection string.")
        return
        
    try:
        logger.info(f"Connecting to SQL Server at {Config.SQL_SERVER}...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        logger.error("Tip: Make sure the database 'DressScraperDB' exists in SQL Server Management Studio.")

def get_db():
    """
    Dependency to get DB session for FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
