from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DATE, TIMESTAMP, CheckConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")

    __table_args__ = (CheckConstraint(role.in_(['admin', 'teacher', 'student'])),)

class Classroom(Base):
    __tablename__ = "classrooms"
    classroom_id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(20), unique=True, nullable=False)
    capacity = Column(Integer)

class Subject(Base):
    __tablename__ = "subjects"
    subject_id = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String(100), unique=True, nullable=False)

class Class(Base):
    __tablename__ = "classes"
    class_id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    classroom_id = Column(Integer, ForeignKey("classrooms.classroom_id"), nullable=False)

    subject = relationship("Subject")
    teacher = relationship("User")
    classroom = relationship("Classroom")

class Enrollment(Base):
    __tablename__ = "enrollments"
    enrollment_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.class_id", ondelete="CASCADE"), nullable=False)
    enrollment_date = Column(DATE, server_default="CURRENT_DATE")

    student = relationship("User")
    class_ = relationship("Class")
    grade = relationship("Grade", uselist=False, back_populates="enrollment")


class Grade(Base):
    __tablename__ = "grades"
    grade_id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.enrollment_id", ondelete="CASCADE"), unique=True, nullable=False)
    grade = Column(DECIMAL(5, 2))
    comments = Column(String)
    last_updated = Column(TIMESTAMP(timezone=True), server_default="CURRENT_TIMESTAMP")

    enrollment = relationship("Enrollment", back_populates="grade")