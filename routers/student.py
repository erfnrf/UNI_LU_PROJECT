from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from models import student as Student
from database import sessionlocal
from schemas import student as sclass
from validators import vc, vf, cc, cities
import re
import models

srouter = APIRouter()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@srouter.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return {"students": students}

@srouter.post("/studentadd")
def add_student(student: sclass, db: Session = Depends(get_db)):
    # Validate student ID
    if student.st[:3] not in ["400", "401", "402"]:
        raise HTTPException(status_code=400, detail="سال وارد شده اشتباه است")
    if student.st[3:9] != "114150":
        raise HTTPException(status_code=400, detail="مثال ما گروه کامپیوتر است 114150")
    if student.st[9:11] == "00":
        raise HTTPException(status_code=400, detail="اندیس 00 قابل قبول نیست")
    
    existing_student = db.query(Student).filter(Student.st == student.st).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="دانشجویی  با این شماره وجود دارد")

    # Validate Persian alphabet for certain fields
    persian_alphabet = list(range(ord('ا'), ord('ی') + 1))
    for attr, name in [("fn", student.fn), ("ln", student.ln), ("f", student.f)]:
        if any(ord(char) not in persian_alphabet for char in name):
            raise HTTPException(status_code=400, detail=f"{attr} باید به فارسی باشد")
        if len(name) > 10:
            raise HTTPException(status_code=400, detail=f"{attr} نباید بیشتر از 10 کاراکتر باشد")

    # Validate birth date
    try:
        year, month, day = map(int, student.birth.split("/"))
    except ValueError:
        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")
    
    if not (1 <= month <= 12) or \
       (month <= 6 and not (1 <= day <= 31)) or \
       (month > 6 and not (1 <= day <= 30)) or \
       (year > 1403):
        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")

    # Validate born city
    if student.borncity not in cities:
        raise HTTPException(status_code=400, detail="شهر وارد شده اشتباه است")
    
    # Validate postal code
    if len(student.postalcode) != 10:
        raise HTTPException(status_code=400, detail="کد پستی باید 10 رقم باشد")
    
    # Validate college and major
    if student.d not in vc:
        raise HTTPException(status_code=400, detail="دانشکده وارد شده اشتباه است")
    if student.m not in vf:
        raise HTTPException(status_code=400, detail="رشته تحصیلی اشتباه است")
    
    # Validate marital status
    if student.ma not in cc:
        raise HTTPException(status_code=400, detail="وضعیت میتواند مجرد یا متاهل باشد")
    
    # Validate national ID
    if len(student.nid) != 10:
        raise HTTPException(status_code=400, detail="کد ملی باید 10 رقم باشد")

    # Validate professor and course
    professor = db.query(models.professor).filter(models.professor.lid == student.lids).first()
    if not professor:
        professor_ids = [prof.lid for prof in db.query(models.professor).all()]
        professor_names = [f"{prof.pfn} {prof.pln}" for prof in db.query(models.professor).all()]
        raise HTTPException(status_code=400, detail=f"استاد وارد شده اشتباه است. لیست کد استاد‌های موجود: {professor_ids}, نام استاد‌ها: {professor_names}")

    course = db.query(models.course).filter(models.course.cid == student.scid).first()
    if not course:
        course_ids = [course.cid for course in db.query(models.course).all()]
        course_names = [course.cname for course in db.query(models.course).all()]
        raise HTTPException(status_code=400, detail=f"درس وارد شده اشتباه است. لیست کد درس‌های موجود: {course_ids}, نام درس‌ها: {course_names}")

    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "student added successfully", "student": new_student}

@srouter.put("/studentupdate/{student_id}")
def update_student(student_id: int, student: sclass, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter(Student.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in student.dict().items():
        setattr(existing_student, key, value)

    db.commit()
    db.refresh(existing_student)
    return {"message": "Student updated successfully", "student": existing_student}

@srouter.delete("/studentdelete/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter(Student.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(existing_student)
    db.commit()
    return {"message": "Student deleted successfully"}
