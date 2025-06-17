# This is the complete content for backend/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, schemas
from .auth import get_password_hash, get_current_admin_user, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# CREATE a new user (admin only)
@router.post("/", response_model=schemas.UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    # Check if user with that email already exists
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
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

# GET all users (admin only)
@router.get("/", response_model=List[schemas.UserDisplay])
def get_all_users(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    users = db.query(models.User).all()
    return users

# GET a specific user by ID (admin only)
@router.get("/{user_id}", response_model=schemas.UserDisplay)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user

# UPDATE a user (admin only)
@router.put("/{user_id}", response_model=schemas.UserDisplay)
def update_user(user_id: int, request: schemas.UserUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    user_query = db.query(models.User).filter(models.User.user_id == user_id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    
    update_data = request.dict(exclude_unset=True)
    user_query.update(update_data)
    db.commit()
    db.refresh(user)
    return user

# DELETE a user (admin only)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    user_query = db.query(models.User).filter(models.User.user_id == user_id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    
    user_query.delete(synchronize_session=False)
    db.commit()
    return

# GET current logged-in user's details
@router.get("/me", response_model=schemas.UserDisplay)
def get_current_user_details(current_user: models.User = Depends(get_current_user)):
    # The get_current_user dependency already fetches the user from the DB
    # so we just have to return it.
    return current_user