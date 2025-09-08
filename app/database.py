from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from .config import settings
import os

DATABASE_URL = (
    f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}"
    f"@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": 10,
        "application_name": "cryptocomics_dex_api"
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Reflect metadata once at startup with error handling
metadata = MetaData()
pool_table = None
transactions_table = None
holders_table = None
pool_tick_table = None

try:
    metadata.reflect(bind=engine)
    pool_table = metadata.tables.get("pool_matrix")
    transactions_table = metadata.tables.get("recent_swaps")
    holders_table = metadata.tables.get("token_holders")
    pool_tick_table = metadata.tables.get("pair_ticks")   
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