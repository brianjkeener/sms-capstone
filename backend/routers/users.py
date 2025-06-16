from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, schemas
from .auth import get_password_hash, get_current_admin_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    hashed_password = get_password_hash(request.password)
    new_user = models.User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password_hash=hashed_password,
        role=request.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.UserDisplay])
def get_all_users(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    users = db.query(models.User).all()
    return users