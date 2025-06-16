# ### This is the ENTIRE content for backend/main.py ###

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models, database
from .config import settings
from .routers import auth, users, classes, grades

# --- Database Initialization ---
# Create the SQLAlchemy engine using the URL from our settings
engine = create_engine(settings.DATABASE_URL)

# Set the SessionLocal in the database module so get_db() can use it
database.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all database tables based on the models
models.Base.metadata.create_all(bind=engine)


# --- FastAPI App Initialization ---
app = FastAPI()

# Configure CORS
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(classes.router)
app.include_router(grades.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Student Management System API"}