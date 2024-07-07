from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from models import course as Course
from database import sessionlocal
from schemas import course as cclass
from validators import vc
import re

crouter = APIRouter()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

def is_valid_cname(cname: str) -> bool:
    pattern = r'^(?=.*[آ-ی])[آ-ی0-9]+$'
    return bool(re.match(pattern, cname))

@crouter.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return {"courses": courses}

@crouter.post("/courseadd")
def add_course(course: cclass, db: Session = Depends(get_db)):
    # Validate course ID
    if len(str(course.cid)) != 5 or not str(course.cid).isdigit():
        raise HTTPException(status_code=400, detail="cid error")
    
    # Check if the course already exists
    course_exists = db.query(Course).filter(Course.cid == course.cid).first()
    if course_exists:
        raise HTTPException(status_code=400, detail="درس وارد شده تکراری است")

    # Validate Persian alphabet for course name
    if len(course.cname) > 25:
        raise HTTPException(status_code=400, detail="بیشتر از 25 کاراکتر است cname")
    
    # Validate cname pattern
    if not is_valid_cname(course.cname):
        raise HTTPException(status_code=400, detail="cname باید حداقل یک حرف فارسی و صفر یا بیشتر عدد داشته باشد")

    # Additional validations
    if course.de not in vc:
        raise HTTPException(status_code=400, detail="رشته مورد نظر اشتباه است course de")
    if course.credit not in ["1", "2", "3", "4"]:
        raise HTTPException(status_code=400, detail="واحد وارد شده اشتباه است course credit")

    # Add course to database
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"message": "Course added successfully", "course": new_course}

@crouter.put("/courseupdate/{course_id}")
def update_course(course_id: int, course: cclass, db: Session = Depends(get_db)):
    existing_course = db.query(Course).filter(Course.id == course_id).first()
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in course.dict().items():
        setattr(existing_course, key, value)

    db.commit()
    db.refresh(existing_course)
    return {"message": "Course updated successfully", "course": existing_course}

@crouter.delete("/coursedelete/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    existing_course = db.query(Course).filter(Course.id == course_id).first()
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(existing_course)
    db.commit()
    return {"message": "Course deleted successfully"}
