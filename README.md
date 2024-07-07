University System Management
This code is designed to manage university system information, including adding professors, students, and course enrollments. It supports both frontend usage for website integration and backend usage with tools like Postman and Insomnia. The code includes validation for all inputs. The data must be entered in the following order: course, professor, then student; otherwise, it won't be accepted. Below, I will demonstrate how to use this code with backend tools.

Project Directory Structure
```
UNI_LU_PROJECT/
├── routers/
│   ├── __pycache__/
│   │   ├── course.cpython-38.pyc
│   │   ├── professor.cpython-38.pyc
│   │   └── student.cpython-38.pyc
│   ├── course.py
│   ├── professor.py
│   └── student.py
├── static/
│   └── style.css
├── templates/
│   ├── addnew.html
│   ├── base.html
│   ├── box.html
│   ├── course.html
│   ├── edit.html
│   ├── editbox.html
│   ├── editprof.html
│   ├── home.html
│   ├── index.html
│   ├── prof.html
│   └── profex.html
├── .gitattributes
├── database.py
├── dockerfile
├── fastapidb.sqlite3
├── main.py
├── models.py
├── README.md
├── requirements.txt
├── schemas.py
└── validators.py

```
## JSON Examples

### For Student
```json
{
    "st": "40211415001",
    "fn": "نام",
    "ln": "نام‌خانوادگی",
    "p": "پدر",
    "birth": "1302/01/31",
    "ids": "98765432101",
    "borncity": "تهران",
    "address": "123 Main St, Apartment 4B",
    "postalcode": "1234512345",
    "cp": "01234567890",
    "hp": "1234567890",
    "de": "فنی و مهندسی",
    "ma": "مهندسی نفت",
    "mjd": "مهندسی نفت",
    "nid": "0250254433",
    "scid": "کد استاد",
    "lids": "کد استاد"
}

```





### For Professor

```json


{
  "lid": "111111",
  "pfn": "اسم",
  "pln": "فامیلی",
  "pbirth": "1383/01/01",
  "pborncity": "تهران",
  "paddress": "123 University St, New York, NY 10001",
  "ppostalcode": "1234512345",
  "pcp": "091919221",
  "php": "+1",
  "php_number": "5551234567",
  "pd":"فنی و مهندسی",
  "pm": "مهندسی نفت",
  "pnid": "A123456789",
  "pscid": "ریاضی"
}

```







### For Course


```json

{
  "cid": "12345",
  "cname": "ریاضی",
  "de": "فنی و مهندسی",
  "credit": "3"
}

```




============================================================================================

```python

from fastapi import FastAPI, Request, Depends, Form, status,HTTPException,APIRouter
from fastapi.templating import Jinja2Templates
import models
import uvicorn
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional
from schemas import student as sclass
from schemas import professor as pclass
from schemas import course as cclass
from models import course, professor
import re
from routers import student as s
from routers import professor as p
from routers import course as c
 
```
### Imports


```python

from fastapi import APIRouter, Response, status, Depends, HTTPException
from models import student
from database import sessionlocal
from schemas import student as sclass
from sqlalchemy.orm import Session
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
    students = db.query(models.student).all()
    return {"students": students}


@srouter.post("/studentadd")
def add_student(student: sclass, db: Session = Depends(get_db)):
    if student.st[:3] not in ["400", "401", "402"]:
        raise HTTPException(status_code=400, detail="سال وارد شده اشتباه است")
    if student.st[3:9] != "114150":
        raise HTTPException(status_code=400, detail="مثال ما گروه کامپیوتر است 114150")
    if student.st[9:11] == "00":
        raise HTTPException(status_code=400, detail="اندیس 00 قابل قبول نیست")

    persian_alphabet = list(range(ord('ا'), ord('ی') + 1))
    for attr, name in [("fn", student.fn), ("ln", student.ln), ("f", student.f)]:
        if any(ord(char) not in persian_alphabet for char in name):
            raise HTTPException(status_code=400, detail=f"{attr} باید به فارسی باشد")
        if len(name) > 10:
            raise HTTPException(status_code=400, detail=f"{attr} نباید بیشتر از 10 کاراکتر باشد")

    try:
        year, month, day = map(int, student.birth.split("/"))
    except ValueError:
        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")

    if not (1 <= month <= 12) or \
       (month <= 6 and not (1 <= day <= 31)) or \
       (month > 6 and not (1 <= day <= 30)) or \
       (year > 1403):
        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")

    if student.borncity not in cities:
        raise HTTPException(status_code=400, detail="شهر وارد شده اشتباه است")
    if len(student.postalcode) != 10:
        raise HTTPException(status_code=400, detail="کد پستی باید 10 رقم باشد")
    if student.d not in vc:
        raise HTTPException(status_code=400, detail="دانشکده وارد شده اشتباه است")
    if student.m not in vf:
        raise HTTPException(status_code=400, detail="رشته تحصیلی اشتباه است")
    if student.ma not in cc:
        raise HTTPException(status_code=400, detail="وضعیت میتواند مجرد یا متاهل باشد")
    if len(student.nid) != 10:
        raise HTTPException(status_code=400, detail="کد ملی باید 10 رقم باشد")

    new_student = models.student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "student added successfully", "student": new_student}

@srouter.put("/studentupdate/{student_id}")
def update_student(student_id: int, student: sclass, db: Session = Depends(get_db)):
    existing_student = db.query(models.student).filter(models.student.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in student.dict().items():
        setattr(existing_student, key, value)

    db.commit()
    db.refresh(existing_student)
    return {"message": "Student updated successfully", "student": existing_student}

@srouter.delete("/studentdelete/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    existing_student = db.query(models.student).filter(models.student.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(existing_student)
    db.commit()
    return {"message": "Student deleted successfully"}




```

### The above section is for retrieving and validating student information.
### The above section is for updating student information.
### The above section is for deleting student information.




 ```python




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


    if len(professor.lid) != 6:
        raise HTTPException(status_code=400, detail="کد استاد 6 رقم است")
    

    for attr, name in [("pfn", professor.pfn), ("pln", professor.pln)]:
        if any(ord(char) not in persian_alphabet for char in name):
            raise HTTPException(status_code=400, detail=f"{attr} باید به فارسی باشد")
        if len(name) > 10:
            raise HTTPException(status_code=400, detail=f"{attr} نباید بیشتر از 10 کاراکتر باشد")


    try:
        year, month, day = map(int, professor.pbirth.split("/"))
    except ValueError:
        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")

    if not (1 <= month <= 12) or \
       (month <= 6 and not (1 <= day <= 31)) or \
       (month > 6 and not (1 <= day <= 30)) or \
       (year > 1403):
        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")

 
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

   
    course_exists = db.query(models.course).filter(models.course.cname == professor.pscid).first()
    if not course_exists:
        
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








```


### The above section is for retrieving and validating professor information.
### The above section is for updating professor information.
### The above section is for deleting professor information.





```python




from fastapi import APIRouter, Response, status, Depends, HTTPException
from models import course
from database import sessionlocal
from schemas import course as cclass
from sqlalchemy.orm import Session
from validators import vc
import re
import models

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
    courses = db.query(models.course).all()
    return {"courses": courses}

@crouter.post("/courseadd")
def add_course(course: cclass, db: Session = Depends(get_db)):
    # Validate course ID
    if len(str(course.cid)) != 5 or not str(course.cid).isdigit():
        raise HTTPException(status_code=400, detail="cid error")

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
    new_course = models.course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"message": "Course added successfully", "course": new_course}

@crouter.put("/courseupdate/{course_id}")
def update_course(course_id: int, course: cclass, db: Session = Depends(get_db)):
    existing_course = db.query(models.course).filter(models.course.id == course_id).first()
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in course.dict().items():
        setattr(existing_course, key, value)

    db.commit()
    db.refresh(existing_course)
    return {"message": "Course updated successfully", "course": existing_course}

@crouter.delete("/coursedelete/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    existing_course = db.query(models.course).filter(models.course.id == course_id).first()
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(existing_course)
    db.commit()
    return {"message": "Course deleted successfully"}


# Include router in the app


```

### The above section is for retrieving and validating course information.
### The above section is for updating course information.
### The above section is for deleting course information.



============================================================================================

```

 ```![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/43d33aca-9811-4e54-b48e-2284e85d43b0)

```

 ```![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/3bb71746-860b-4277-ae90-cb26ee326333)

```

 ```![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/62a63d50-32b7-4a60-848f-e60291f9fb95)

```

 ```![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/dd28ef6e-3170-49e2-baec-0639db55be4a)



### These sections specify the data states received and stored in our database. The database expects to receive these data.


============================================================================================


```

 ```![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/b4fd1a18-5b14-422a-b231-9803f272dad4)


```

 ```![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/ca2e630c-9b3d-413d-8986-db42e02a5a48)


```

 ```![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/e08fc922-d739-44ac-8114-559c6cd59323)

### data

============================================================================================

```

 ```![image](https://github.com/erfnrf/UNI_LU_PROJECT/assets/142250364/308a8747-3854-4c01-854e-56d3367a5dce)


### Main File







============================================================================================

