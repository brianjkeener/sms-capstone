# This is the complete content for backend/routers/classes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, schemas
from .auth import get_current_admin_user, get_current_teacher_user

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

# NEW ENDPOINT: Get classes for the currently logged-in teacher
@router.get("/me", response_model=List[schemas.ClassBasicDisplay])
def get_my_classes(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_teacher_user)):
    classes = db.query(models.Class)\
        .join(models.Subject).join(models.Classroom)\
        .filter(models.Class.teacher_id == current_user.user_id).all()
    
    # Manually construct the response to match the schema
    response = []
    for c in classes:
        response.append({
            "class_id": c.class_id,
            "subject_name": c.subject.subject_name,
            "room_number": c.classroom.room_number
        })
    return response

# NEW ENDPOINT: Get all students enrolled in a specific class
@router.get("/{class_id}/students", response_model=List[schemas.EnrolledStudentDisplay])
def get_students_in_class(class_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_teacher_user)):
    # First, ensure the class exists and the current teacher is assigned to it
    class_obj = db.query(models.Class).filter(models.Class.class_id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    if class_obj.teacher_id != current_user.user_id and current_user.role != 'admin':
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this class")

    # Get all enrollments for this class and join with user and grade info
    enrollments = db.query(models.Enrollment)\
        .join(models.User)\
        .outerjoin(models.Grade)\
        .filter(models.Enrollment.class_id == class_id).all()

    # Manually construct the response
    response = []
    for e in enrollments:
        response.append({
            "user_id": e.student.user_id,
            "first_name": e.student.first_name,
            "last_name": e.student.last_name,
            "grade": e.grade.grade if e.grade else None,
            "comments": e.grade.comments if e.grade else None
        })
    return response