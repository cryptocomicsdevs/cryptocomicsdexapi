from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
import os

DATABASE_URL = (
    f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}"
    f"@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Reflect metadata once at startup with error handling
metadata = MetaData()
pool_table = None
transactions_table = None
holders_table = None

try:
    metadata.reflect(bind=engine)
    pool_table = metadata.tables.get("pool_matrix")
    transactions_table = metadata.tables.get("recent_swaps")
    holders_table = metadata.tables.get("token_holders")
    print("Database connection successful - tables reflected")
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Server will start but database endpoints may not work")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()