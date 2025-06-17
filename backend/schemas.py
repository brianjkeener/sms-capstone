from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

# ---- User ----
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str
    role: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None

class UserDisplay(UserBase):
    user_id: int
    role: str
    
    class Config:
        orm_mode = True

# ---- Auth ----
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ---- Grade ----
class GradeBase(BaseModel):
    grade: float
    comments: Optional[str] = None

class GradeCreate(GradeBase):
    student_id: int
    class_id: int

class GradeDisplay(GradeBase):
    subject_name: str
    teacher_name: str

    class Config:
        orm_mode = True
        
# ---- Class ----
class ClassBase(BaseModel):
    subject_id: int
    teacher_id: int
    classroom_id: int

class ClassCreate(ClassBase):
    pass

class ClassDisplay(BaseModel):
    class_id: int
    subject_name: str
    teacher_name: str
    room_number: str
    
    class Config:
        orm_mode = True

class ClassBasicDisplay(BaseModel):
    class_id: int
    subject_name: str
    room_number: str
    
    class Config:
        from_attributes = True

class EnrolledStudentDisplay(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    grade: Optional[float] = None
    comments: Optional[str] = None

    class Config:
        from_attributes = True