from sqlalchemy.orm import sessionmaker, declarative_base

# NOTE: The engine is now created in main.py
# This file now only defines the building blocks.

SessionLocal = None
Base = declarative_base()

def get_db():
    if SessionLocal is None:
        raise Exception("Database session not initialized.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()