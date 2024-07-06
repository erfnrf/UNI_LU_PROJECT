from typing import Union

from pydantic import BaseModel,Field
from typing import Optional

class student(BaseModel):
    st:str = Field(..., max_length=11)
    fn:str = Field(..., max_length=10)
    ln:str = Field(..., max_length=10)
    f: str= Field(..., max_length=10)
    birth: str = Field(..., max_length=10)
    ids: str = Field(..., max_length=11)
    borncity:str = Field(..., max_length=150)
    address: str= Field(..., max_length=100)
    postalcode:str = Field(..., max_length=10)
    cp: str = Field(..., max_length=11)
    hp: str= Field(..., max_length=10)
    d: str= Field(..., max_length=150)
    m:str = Field(..., max_length=150)
    ma:str = Field(..., max_length=150)
    nid:str = Field(..., max_length=150)
    scid: str = Field(..., max_length=150)
    lids: str = Field(..., max_length=150)

class studentadd(student):
    pass

class studentid(student):
    id: int

class professor(BaseModel):
    lid: str = Field(..., max_length=6)
    pfn: str = Field(..., max_length=10)
    pln: str = Field(..., max_length=10)
    pbirth: str = Field(..., max_length=10)
    pborncity: str = Field(..., max_length=150)
    paddress: str = Field(..., max_length=100)
    ppostalcode: str = Field(..., max_length=10)
    pcp: str = Field(..., max_length=11)
    php: str = Field(..., max_length=10)
    php_number: str = Field(..., max_length=10)
    pd: str = Field(..., max_length=30)
    pm: str = Field(..., max_length=30)
    pnid: str = Field(..., max_length=10)
    pscid: str = Field(..., max_length=150)

class professoradd(professor):
    pass

class professorid(professor):
    id: int

class course(BaseModel):
    cid: int
    cname: str
    de: str
    credit: str

class coursecreate(course):
    pass

class courseid(course):
    id: int