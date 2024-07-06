from fastapi import APIRouter, Response, status, Depends, HTTPException
from models import professor
from database import sessionlocal
from schemas import professor as pclass
from sqlalchemy.orm import Session
from validators import vc, vf, cc, cities
import re
import models

prouter = APIRouter()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@prouter.get("/professors")
def get_professors(db: Session = Depends(get_db)):
    professors = db.query(models.professor).all()
    return {"professors": professors}
@prouter.post("/professoradd")
def add_professor(professor: pclass, db: Session = Depends(get_db)):
    persian_alphabet = list(range(ord('ا'), ord('ی') + 1))

    # Validate professor ID length
    if len(professor.lid) != 6:
        raise HTTPException(status_code=400, detail="کد استاد 6 رقم است")
    
    # Validate Persian alphabet for names
    for attr, name in [("pfn", professor.pfn), ("pln", professor.pln)]:
        if any(ord(char) not in persian_alphabet for char in name):
            raise HTTPException(status_code=400, detail=f"{attr} باید به فارسی باشد")
        if len(name) > 10:
            raise HTTPException(status_code=400, detail=f"{attr} نباید بیشتر از 10 کاراکتر باشد")

    # Validate birth date format
    try:
        year, month, day = map(int, professor.pbirth.split("/"))
    except ValueError:
        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")

    if not (1 <= month <= 12) or \
       (month <= 6 and not (1 <= day <= 31)) or \
       (month > 6 and not (1 <= day <= 30)) or \
       (year > 1403):
        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")

    # Additional validations
    if professor.pborncity not in cities:
        raise HTTPException(status_code=400, detail="شهر وارد شده اشتباه است")
    if len(professor.ppostalcode) != 10:
        raise HTTPException(status_code=400, detail="کد پستی باید 10 رقم باشد")
    if professor.pd not in vc:
        raise HTTPException(status_code=400, detail="دانشکده وارد شده اشتباه است")
    if professor.pm not in vf:
        raise HTTPException(status_code=400, detail="رشته تحصیلی اشتباه است")
    if len(professor.pnid) != 10:
        raise HTTPException(status_code=400, detail="کد ملی باید 10 رقم باشد")

    # Check if pscid exists in the course table
    course_exists = db.query(models.course).filter(models.course.cname == professor.pscid).first()
    if not course_exists:
        # Get list of all course names
        course_names = [course.cname for course in db.query(models.course).all()]
        raise HTTPException(status_code=400, detail=f"درس مورد نظر اشتباه است. لیست درس‌های موجود: {course_names}")

    # Add professor to database
    new_professor = models.professor(**professor.dict())
    db.add(new_professor)
    db.commit()
    db.refresh(new_professor)
    return {"message": "professor added successfully", "professor": new_professor}

def is_valid_cname(cname: str) -> bool:
    pattern = r'^(?=.*[آ-ی])[آ-ی0-9]+$'
    return bool(re.match(pattern, cname))

@prouter.put("/professorupdate/{professor_id}")
def update_professor(professor_id: int, professor: pclass, db: Session = Depends(get_db)):
    existing_professor = db.query(models.professor).filter(models.professor.id == professor_id).first()
    if not existing_professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    for key, value in professor.dict().items():
        setattr(existing_professor, key, value)

    db.commit()
    db.refresh(existing_professor)
    return {"message": "Professor updated successfully", "professor": existing_professor}

@prouter.delete("/professordelete/{professor_id}")
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    existing_professor = db.query(models.professor).filter(models.professor.id == professor_id).first()
    if not existing_professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    db.delete(existing_professor)
    db.commit()
    return {"message": "Professor deleted successfully"}



# Include router in the app
