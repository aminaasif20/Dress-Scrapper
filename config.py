import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "2.0"))
    
    # MS SQL Server Connection Details
    # Default assumes Windows Authentication (Trusted_Connection=yes) to local SQLEXPRESS
    SQL_SERVER = os.getenv("SQL_SERVER", r"AMINA\MSSQLSERVER01") 
    SQL_DATABASE = os.getenv("SQL_DATABASE", "DressScraperDB")
    
    # SQLAlchemy Database URL for pyodbc
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        f"mssql+pyodbc://@{SQL_SERVER}/{SQL_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
    )
