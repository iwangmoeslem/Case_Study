# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Adjust your DB connection string
DATABASE_URL = "postgresql://postgres:@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables (only needed once)
def init_db():
    Base.metadata.create_all(bind=engine)
