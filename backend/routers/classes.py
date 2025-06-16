from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, schemas
from .auth import get_current_admin_user

router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)

@router.post("/", response_model=schemas.ClassCreate, status_code=status.HTTP_201_CREATED)
def create_class(request: schemas.ClassCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    new_class = models.Class(**request.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

@router.post("/{class_id}/enroll", status_code=status.HTTP_201_CREATED)
def enroll_student_in_class(class_id: int, student_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_admin_user)):
    # Check if student and class exist
    student = db.query(models.User).filter(models.User.user_id == student_id, models.User.role == 'student').first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    class_obj = db.query(models.Class).filter(models.Class.class_id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    new_enrollment = models.Enrollment(student_id=student_id, class_id=class_id)
    db.add(new_enrollment)
    db.commit()
    return {"message": "Student successfully enrolled"}