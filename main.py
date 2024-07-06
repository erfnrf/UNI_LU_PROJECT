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






#from routers import user, puser, other_user
app = FastAPI()
router = APIRouter()
app.include_router(s.srouter)
app.include_router(p.prouter)
app.include_router(c.crouter)

##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################



#######هستش و ربطی به پروژه نداره frontend ادامه اینجا برای#################
#######هستش و ربطی به پروژه نداره frontend ادامه اینجا برای#################
#######هستش و ربطی به پروژه نداره frontend ادامه اینجا برای#################
#######هستش و ربطی به پروژه نداره frontend ادامه اینجا برای#################
#######هستش و ربطی به پروژه نداره frontend ادامه اینجا برای#################
#######هستش و ربطی به پروژه نداره frontend ادامه اینجا برای#################
#######هستش و ربطی به پروژه نداره frontend ادامه اینجا برای#################
#######هستش و ربطی به پروژه نداره frontend ادامه اینجا برای#################






##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
##############################################
# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

# Define router


@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

##############################################
vc = ["فنی و مهندسی","علوم پایه","علوم انسانی","دامپزشکی","اقتصاد","کشاورزی","منابع طبیعی"]
vf = ["مهندسی برق - سامانه های برقی حمل و نقل","مهندسی برق","مهندسی صنایع - کیفیت و بهره وری",
                "مهندسی صنایع - مدیریت مهندسی","مهندسی صنایع - مهندسی صنایع","مهندسی صنایع ـ مدیریت سیستم و بهره وری",
                "مهندسی  صنایع","مهندسی  پزشکی  - بیوالکتریک","مهندسی پزشکی - بیومتریال","مهندسی پزشکی - توانبخشی",
                "مهندسی پزشکی - مهندسی توانبخشی","مهندسی پزشکی","مهندسی عمران - ژئوتکنیک","مهندسی عمران - مدیریت ساخت",
                "مهندسی عمران - مهندسی راه و ترابری","مهندسی عمران - مهندسی و مدیریت ساخت","مهندسی عمران",
                "مهندسی فناوری اطلاعات - تجارت الکترونیکی","مهندسی فناوری اطلاعات - شبکه های کامپیوتری",
                "مهندسی کامپیوتر- معماری سیستم های کامپیوتری","مهندسی کامپیوتر- نرم افزار",
                "مهندسی کامپیوتر - هوش مصنوعی و رباتیک","مهندسی فناوری اطلاعات","مهندسی کامپیوتر - فناوری اطلاعات",
                "مهندسی کامپیوتر","مهندسی حرفه ای کامپیوتر نرم افزار", "مهندسی معدن - استخراج مواد معدنی",
                "مهندسی مکاترونیک","مهندسی مکانیک - تبدیل انرژی","مهندسی مکانیک","مهندسی شیمی - طراحی فرآیند",
                "مهندسی شیمی - محیط زیست","مهندسی نفت"
                ]
cc = ["متاهل","مجرد"]
cities = [
    "تبریز", "آذرشهر", "مراغه", "ملکان", "میانه", "هریس", "شبستر", "سراب", "اهر", "خوی", "بستان‌آباد",
    "ارومیه", "خوی", "مهاباد", "بوکان", "نقده", "میاندوآب", "سردشت", "پیرانشهر", "چالدران", "شاهین‌دژ",
    "اردبیل", "مشگین‌شهر", "خلخال", "ارشق", "کوثر", "نمین", "نیر",
    "اصفهان", "کاشان", "نجف‌آباد", "اردستان", "شهرضا", "گلپایگان", "لنجان", "خمینی‌شهر", "فریدن", "فلاورجان", "تیران و کرون", "چادگان", "برخوار",
    "ایلام", "دهلران", "مهران", "چرداول", "ایوان",
    "بوشهر", "گناوه", "دیلم", "دشتستان", "دیر", "تنگستان", "خورموج",
    "تهران", "شهریار", "ملارد", "پاکدشت", "ری", "شمیرانات", "ورامین", "قدس",
    "شهرکرد", "بروجن", "کوهرنگ", "لردگان", "فارسان", "بن", "آلونی",
    "بیرجند", "زیرکوه", "نهبندان", "درمیان", "سرایان", "سربیشه", "قائنات",
    "مشهد", "تربت حیدریه", "سبزوار", "نیشابور", "تربت جام", "قوچان", "گناباد", "خواف", "کاشمر", "سرخس", "رشتخوار", "فریمان",
    "بجنورد", "شیروان", "اسفراین", "گرمه", "راز و جرگلان",
    "اهواز", "ابوموسی", "اندیمشک", "اهرم", "باغ‌ملک", "بندرامام خمینی", "بندرماهشهر", "هندیجان", "حمیدیه", "دزفول", "رامهرمز", "مسجدسلیمان", "ملاثانی", "شادگان", "گتوند", "لالی", "مسعودیه", "هویزه", "خرمشهر", "کوت عبدالله", "آبادان", "شوش", "چغامیش", "رامشیر", "امیدیه", "مینوشهر",
    "سمنان", "شاهرود", "گرمسار", "دامغان", "سرخه",
    "زاهدان", "چابهار", "خاش", "ایرانشهر", "سراوان", "نیک‌شهر", "زابل", "دلگان", "کنارک", "هامون", "میرجاوه", "سیب و سوران", "قصرقند",
    "شیراز", "مرودشت", "کازرون", "فسا", "جهرم", "لارستان", "خرم‌بید", "استهبان", "مهر", "ممسنی", "رستم", "فیروزآباد", "نی‌ریز",
    "قزوین", "آبیک", "آوج", "بوئین‌زهرا", "تاکستان",
    "قم","جیرفت",
    "سنندج", "مریوان", "بانه", "سقز", "دیواندره", "سروآباد", "قروه", "کامیاران", "کرمانشاه",
    "کرمان", "بم", "رفسنجان", "سیرجان", "زرند", "شهربابک", "بافت", "کهنوج", "راور", "سرچشمه", "رابر", "فهرج", "انار",
    "کرمانشاه", "کنگاور", "سنقر", "قصرشیرین", "هرسین", "صحنه", "پاوه", "جوانرود", "گیلانغرب", "روانسر", "دالاهو",
    "یاسوج", "دهدشت", "گچساران", "باشت", "چرام", "لنده",
    "رشت", "بندرانزلی", "آستارا", "لاهیجان", "ماسال", "املش", "فومن", "رودسر", "لنگرود",
    "گرگان", "گنبدکاووس", "آق‌قلا", "مینودشت", "گالیکش", "علی‌آباد", "گمیش‌تپه", "ترکمن", "کردکوی",
    "خرم‌آباد", "بروجرد", "دورود", "ازنا", "الیگودرز", "کوهدشت", "الشتر",
    "ساری", "بابل", "بابلسر", "آمل", "نور", "چالوس", "قائم‌شهر", "جویبار", "نکا", "کلاردشت", "محمودآباد", "رامسر", "سوادکوه",
    "اراک", "خمین", "محلات", "تفرش", "کمیجان", "شازند", "ساوه",
    "بندرعباس", "بندرلنگه", "قشم", "میناب", "جاسک", "حاجی‌آباد", "رودان", "دشتی", "بشاگرد", "چابکسر",
    "همدان", "ملایر", "نهاوند", "تویسرکان", "رزن", "بهار", "کرج", "نظرآباد", "مهرشهر", "ماهدشت", "اشتهارد", "طالقان", "چهارباغ", "فردیس", "اندیشه", "شهریار", "کبودرآهنگ",
    "یزد", "اردکان", "بافق", "تفت", "مهریز", "اشکذر", "خاتم", "ابرکوه", "اردستان", "بهاباد", "ادبیه"
]











###############################################
# Home route
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    students = db.query(models.student).order_by(models.student.id.desc()).all()
    return templates.TemplateResponse("home.html", {"request": request, "students": students})

@app.get("/home")
async def home(request: Request, db: Session = Depends(get_db)):
    students = db.query(models.student).order_by(models.student.id.desc()).all()
    return templates.TemplateResponse("home.html", {"request": request, "students": students})

# Students routes
@app.get("/index")
@app.get("/studentsinfo")
async def students_info(request: Request, db: Session = Depends(get_db)):
    students = db.query(models.student).order_by(models.student.id.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "students": students})

@app.post("/add")
async def add_student(request: Request, 
                      st: str = Form(...), fn: str = Form(...), ln: str = Form(...), f: str = Form(...), 
                      birth: str = Form(...), ids: str = Form(...), borncity: str = Form(...), address: str = Form(...), 
                      postalcode: str = Form(...), cp: str = Form(...), hp: str = Form(...), d: str = Form(...), 
                      m: str = Form(...), ma: str = Form(...), nid: str = Form(...), scid: str = Form(...), 
                      lids: str = Form(...), db: Session = Depends(get_db)):
    new_student = models.student(st=st, fn=fn, ln=ln, f=f, birth=birth, ids=ids, borncity=borncity, address=address, postalcode=postalcode, cp=cp, hp=hp, d=d, m=m, ma=ma, nid=nid, scid=scid, lids=lids)
    db.add(new_student)
    db.commit()
    return RedirectResponse(url=app.url_path_for("students_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/studentsadd")
async def add_student_form(request: Request , db: Session = Depends(get_db)):
    professors = db.query(professor).all()
    courses = db.query(course).all()
    return templates.TemplateResponse("addnew.html", {"request": request, "professors": professors,  "courses": courses})


@app.get("/edit_student/{user_id}")
async def edit_student(request: Request, user_id: int, db: Session = Depends(get_db)):
    student = db.query(models.student).filter(models.student.id == user_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "user": student})

@app.post("/update_student/{user_id}")
async def update_student(request: Request, user_id: int, st: str = Form(...), fn: str = Form(...), ln: str = Form(...), f: str = Form(...), birth: str = Form(...), ids: str = Form(...), borncity: str = Form(...), address: str = Form(...), postalcode: str = Form(...), cp: str = Form(...), hp: str = Form(...), d: str = Form(...), m: str = Form(...), ma: str = Form(...), nid: str = Form(...), scid: str = Form(...), lids: str = Form(...), db: Session = Depends(get_db)):
    student = db.query(models.student).filter(models.student.id == user_id).first()
    student.st = st
    student.fn = fn
    student.ln = ln
    student.f = f
    student.birth = birth
    student.ids = ids
    student.borncity = borncity
    student.address = address
    student.postalcode = postalcode
    student.cp = cp
    student.hp = hp
    student.d = d
    student.m = m
    student.ma = ma
    student.nid = nid
    student.scid = scid
    student.lids = lids
    db.commit()
    return RedirectResponse(url=app.url_path_for("students_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete_student/{user_id}")
async def delete_student(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.student).filter(models.student.id == user_id).first()
    db.delete(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("students_info"), status_code=status.HTTP_303_SEE_OTHER)

# Courses routes
@app.get("/box")
@app.get("/coursesinfo")
async def courses_info(request: Request, db: Session = Depends(get_db)):
    courses = db.query(models.course).order_by(models.course.id.desc()).all()
    return templates.TemplateResponse("box.html", {"request": request, "courses": courses})

@app.post("/add_course")
async def add_course(request: Request, cid: int = Form(...), cname: str = Form(...), de: str = Form(...), credit: str = Form(...), db: Session = Depends(get_db)):
    courses = models.course(cid=cid, cname=cname, de=de, credit=credit)
    db.add(courses)
    db.commit()
    return RedirectResponse(url=app.url_path_for("courses_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/coursesadd")
async def add_course_form(request: Request):
    return templates.TemplateResponse("course.html", {"request": request})

@app.get("/edit_course/{user_id}")
async def edit_course(request: Request, user_id: int, db: Session = Depends(get_db)):
    course = db.query(models.course).filter(models.course.id == user_id).first()
    return templates.TemplateResponse("editbox.html", {"request": request, "user": course})

@app.post("/update_course/{user_id}")
async def update_course(request: Request, user_id: int, cid: int = Form(...), cname: str = Form(...), de: str = Form(...), credit: str = Form(...), db: Session = Depends(get_db)):
    other_user = db.query(models.course).filter(models.course.id == user_id).first()
    other_user.cid = cid
    other_user.cname = cname
    other_user.de = de
    other_user.credit = credit
    db.commit()
    return RedirectResponse(url=app.url_path_for("courses_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete_course/{user_id}")
async def delete_course(request: Request, user_id: int, db: Session = Depends(get_db)):
    other_user = db.query(models.course).filter(models.course.id == user_id).first()
    db.delete(other_user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("courses_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/professorsinfo")
async def professors_info(request: Request, db: Session = Depends(get_db)):
    professors = db.query(models.professor).order_by(models.professor.id.desc()).all()
    return templates.TemplateResponse("profex.html", {"request": request, "professors": professors})

@app.post("/add_professor")
async def add_professor(request: Request, 
                        lid: str = Form(...), pfn: str = Form(...), pln: str = Form(...), 
                        pbirth: str = Form(...), pborncity: str = Form(...), paddress: str = Form(...), 
                        ppostalcode: str = Form(...), pcp: str = Form(...), php: str = Form(...), php_number: str = Form(...), pd: str = Form(...), 
                        pm: str = Form(...), pnid: str = Form(...), pscid: str = Form(...), 
                        db: Session = Depends(get_db)):
    
    professors = models.professor(lid=lid, pfn=pfn, pln=pln, pbirth=pbirth, pborncity=pborncity, paddress=paddress, ppostalcode=ppostalcode, pcp=pcp, php=php, php_number=php_number, pd=pd, pm=pm, pnid=pnid, pscid=pscid)
    db.add(professors)
    db.commit()
    return RedirectResponse(url=app.url_path_for("professors_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/professoradd")
async def add_professor_form(request: Request, db: Session = Depends(get_db)):
    courses = db.query(course).all()  # Fetch all courses
    return templates.TemplateResponse("prof.html", {"request": request, "courses": courses})

@app.get("/edit_professor/{user_id}")
async def edit_professor(request: Request, user_id: int, db: Session = Depends(get_db)):
    professor = db.query(models.professor).filter(models.professor.id == user_id).first()
    return templates.TemplateResponse("editprof.html", {"request": request, "user": professor})

@app.post("/update_professor/{user_id}")
async def update_professor(request: Request, user_id: int, php_number: str = Form(...), lid: str = Form(...), pfn: str = Form(...), pln: str = Form(...), pbirth: str = Form(...), pborncity: str = Form(...), paddress: str = Form(...), ppostalcode: str = Form(...), pcp: str = Form(...), php: str = Form(...), pd: str = Form(...), pm: str = Form(...), pnid: str = Form(...), pscid: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.professor).filter(models.professor.id == user_id).first()
    user.lid = lid
    user.pfn = pfn
    user.pln = pln
    user.pbirth = pbirth
    user.pborncity = pborncity
    user.paddress = paddress
    user.ppostalcode = ppostalcode
    user.pcp = pcp
    user.php = php
    user.php_number = php_number
    user.pd = pd
    user.pm = pm
    user.pnid = pnid
    user.pscid = pscid
    db.commit()
    return RedirectResponse(url=app.url_path_for("professors_info"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete_professor/{user_id}")
async def delete_professor(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.professor).filter(models.professor.id == user_id).first()
    db.delete(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("professors_info"), status_code=status.HTTP_303_SEE_OTHER)

# Pydantic model for test course
#@app.post("/studentadd")
#def add_student(student: sclass, db: Session = Depends(get_db)):
#    if student.st[:3] not in ["400", "401", "402"]:
#        raise HTTPException(status_code=400, detail="سال وارد شده اشتباه است")
#    if student.st[3:9] != "114150":
#        raise HTTPException(status_code=400, detail="مثال ما گروه کامپیوتر است 114150")
#    if student.st[9:11] == "00":
#        raise HTTPException(status_code=400, detail="اندیس 00 قابل قبول نیست")
#
#    persian_alphabet = list(range(ord('ا'), ord('ی') + 1))
#    for char in student.fn:
#        if ord(char) not in persian_alphabet:
#            raise HTTPException(status_code=400, detail="نام باید به فارسی باشد")
#
#    if len(student.fn) > 10:
#        raise HTTPException(status_code=400, detail="نام نباید بیشتر از 10 کاراکتر باشد")
#    for char in student.ln:
#        if ord(char) not in persian_alphabet:
#            raise HTTPException(status_code=400, detail="نام خانوادگی باید به فارسی باشد")
#
#    if len(student.ln) > 10:
#        raise HTTPException(status_code=400, detail="نام خانوادگی نباید بیشتر از 10 کاراکتر باشد")
#    for char in student.f:
#        if ord(char) not in persian_alphabet:
#            raise HTTPException(status_code=400, detail="نام پدر باید به فارسی باشد")
#
#    if len(student.f) > 10:
#        raise HTTPException(status_code=400, detail="نام پدر نباید بیشتر از 10 کاراکتر باشد")
#    
#    try:
#        year, month, day = map(int, student.birth.split("/"))
#    except ValueError:
#        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")
#
#    if not (1 <= month <= 12):
#        raise HTTPException(status_code=400, detail="ماه وارد شده نامعتبر است")
#    if month <= 6 and not (1 <= day <= 31):
#        raise HTTPException(status_code=400, detail="روز وارد شده برای ماه‌های اول سال نامعتبر است")
#    if month > 6 and not (1 <= day <= 30):
#        raise HTTPException(status_code=400, detail="روز وارد شده برای ماه‌های دوم سال نامعتبر است")
#    if year > 1403:
#        raise HTTPException(status_code=400, detail="سال وارد شده باید کمتر از 1403 باشد")
#    
#    if student.borncity not in cities:
#        raise HTTPException(status_code=400, detail="شهر وارد شده اشتباه است")
#    if len(student.postalcode) != 10:
#        raise HTTPException(status_code=400, detail="کد پستی باید 10 رقم باشد")
#    if student.d not in vc:
#        raise HTTPException(status_code=400, detail="دانشکده وارد شده اشتباه است")
#    if student.m not in vf:
#        raise HTTPException(status_code=400 , detail="رشته تحصیلی اشتباه است")
#    if student.ma not in cc:
#        raise HTTPException(status_code=400 , detail="وضعیت میتواند مجرد یا متاهل باشد")
#    if len(student.nid) != 10:
#        raise HTTPException(status_code=400 , detail="کد ملی باید 10 رقم باشد")
#
#
#    new_student = models.student(st=student.st, fn=student.fn, ln=student.ln, f=student.f, birth=student.birth, ids=student.ids, borncity=student.borncity, address=student.address, postalcode=student.postalcode, cp=student.cp, hp=student.hp, d=student.d, m=student.m, ma=student.ma, nid=student.nid, scid=student.scid, lids=student.lids)
#    db.add(new_student)
#    db.commit()
#    return {"message": "student added successfully", "student":student}
#
#@app.post("/professoradd")
#def test_professor(professor: pclass, db: Session = Depends(get_db)):
#    persian_alphabet = list(range(ord('ا'), ord('ی') + 1))
#    if len(professor.lid)!=6:
#        raise HTTPException(status_code=400,detail="کد استاد 6 رقم است")
#
#    for char in professor.pfn:
#        if ord(char) not in persian_alphabet:
#            raise HTTPException(status_code=400, detail="نام باید به فارسی باشد")
#
#    if len(professor.pfn) > 10:
#        raise HTTPException(status_code=400, detail="نام نباید بیشتر از 10 کاراکتر باشد")
#
#    for char in professor.pln:
#        if ord(char) not in persian_alphabet:
#            raise HTTPException(status_code=400, detail="نام خانوادگی باید به فارسی باشد")
#
#    if len(professor.pln) > 10:
#        raise HTTPException(status_code=400, detail="نام خانوادگی نباید بیشتر از 10 کاراکتر باشد")
#
#    try:
#        year, month, day = map(int, professor.pbirth.split("/"))
#    except ValueError:
#        raise HTTPException(status_code=400, detail="تاریخ تولد نامعتبر است")
#
#    if not (1 <= month <= 12):
#        raise HTTPException(status_code=400, detail="ماه وارد شده نامعتبر است")
#
#    if month <= 6 and not (1 <= day <= 31):
#        raise HTTPException(status_code=400, detail="روز وارد شده برای ماه‌های اول سال نامعتبر است")
#    elif month > 6 and not (1 <= day <= 30):
#        raise HTTPException(status_code=400, detail="روز وارد شده برای ماه‌های دوم سال نامعتبر است")
#
#    if year > 1403:
#        raise HTTPException(status_code=400, detail="سال وارد شده باید کمتر از 1403 باشد")
#
#    if professor.pborncity not in cities:
#        raise HTTPException(status_code=400, detail="شهر وارد شده اشتباه است")
#
#    if len(professor.ppostalcode) != 10:
#        raise HTTPException(status_code=400, detail="کد پستی باید 10 رقم باشد")
#
#    if professor.pd not in vc:
#        raise HTTPException(status_code=400, detail="دانشکده وارد شده اشتباه است")
#
#    if professor.pm not in vf:
#        raise HTTPException(status_code=400, detail="رشته تحصیلی اشتباه است")
#
#    if len(professor.pnid) != 10:
#        raise HTTPException(status_code=400, detail="کد ملی باید 10 رقم باشد")
#    new_professor = models.professor(lid=professor.lid, pfn=professor.pfn, pln=professor.pln, pbirth=professor.pbirth, pborncity=professor.pborncity, paddress=professor.paddress, ppostalcode=professor.ppostalcode, pcp=professor.pcp, php=professor.php, php_number=professor.php_number, pd=professor.pd, pm=professor.pm, pnid=professor.pnid, pscid=professor.pscid)
#    db.add(new_professor)
#    db.commit()
#    return {"message": "professor added successfully", "professor": professor}
#
#
#@app.post("/courseadd")
#def test_courses(course: cclass, db: Session = Depends(get_db)):
#    if len(course.cid) != 5:
#        raise HTTPException(status_code=400, detail="cid error")
#    if not all(char in "0123456789" for char in course.cid):
#        raise HTTPException(status_code=400, detail="cid error")
#    
#    # Persian alphabet range in Unicode
#    persian_alphabet = list(range(ord('ا'), ord('ی') + 1))
#    for char in course.cname:
#        if ord(char) not in persian_alphabet:
#            raise HTTPException(status_code=400, detail="فارسی نیست  cname")
#
#    if len(course.cname) > 25:
#        raise HTTPException(status_code=400, detail="بیشتر از 25 کاراکتر است  cname")
#    
#    if course.de not in vc:
#        raise HTTPException(status_code=400, detail="رشته مورد نظر اشتباه است course de")
#
#    if course.credit not in ["1", "2", "3", "4"]:
#        raise HTTPException(status_code=400, detail="واحد وارد شده اشتباه است course credit")
#
#    new_course = models.course(cid=course.cid, cname=course.cname, de=course.de, credit=course.credit)
#    
#    db.add(new_course)
#    db.commit()
#    db.refresh(new_course)
#    
#    return {"message": "Course added successfully", "course": new_course}


# Include router in the app


uvicorn.run(app, host="127.0.0.1", port=8000)
