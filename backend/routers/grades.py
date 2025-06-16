from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from .. import database, models, schemas
from .auth import get_current_teacher_user, get_current_user

router = APIRouter(
    prefix="/grades",
    tags=["Grades"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_grade(request: schemas.GradeCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_teacher_user)):
    # Find the enrollment for this student in this class
    enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == request.student_id,
        models.Enrollment.class_id == request.class_id
    ).first()

    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student is not enrolled in this class.")

    # Check if a grade already exists, if so update it (upsert logic)
    grade = db.query(models.Grade).filter(models.Grade.enrollment_id == enrollment.enrollment_id).first()
    if grade:
        grade.grade = request.grade
        grade.comments = request.comments
        grade.last_updated = func.now()
    else:
        new_grade = models.Grade(
            enrollment_id=enrollment.enrollment_id,
            grade=request.grade,
            comments=request.comments
        )
        db.add(new_grade)
    
    db.commit()
    return {"message": "Grade submitted successfully"}


@router.get("/me", response_model=List[schemas.GradeDisplay])
def view_my_grades(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != 'student':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can view their own grades.")

    grades = db.query(
        models.Subject.subject_name,
        models.User.first_name.concat(' ').concat(models.User.last_name).label("teacher_name"),
        models.Grade.grade,
        models.Grade.comments
    ).join(models.Enrollment, models.Grade.enrollment_id == models.Enrollment.enrollment_id)\
     .join(models.Class, models.Enrollment.class_id == models.Class.class_id)\
     .join(models.Subject, models.Class.subject_id == models.Subject.subject_id)\
     .join(models.User, models.Class.teacher_id == models.User.user_id)\
     .filter(models.Enrollment.student_id == current_user.user_id).all()
    
    return grades