from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    st = Column(String(11), nullable=False)
    fn = Column(String(10), nullable=False)
    ln = Column(String(10), nullable=False)
    f = Column(String(10), nullable=False)
    birth = Column(String(10), nullable=False)
    ids = Column(String(11), nullable=False)
    borncity = Column(String(150), nullable=False)
    address = Column(String(100), nullable=False)
    postalcode = Column(String(10), nullable=False)
    cp = Column(String(11), nullable=False)
    hp = Column(String(10), nullable=False)
    d = Column(String(150), nullable=False)
    m = Column(String(150), nullable=False)
    ma = Column(String(150), nullable=False)
    nid = Column(String(150), nullable=False)
    scid = Column(String(150), nullable=False)
    lids = Column(String(150), nullable=False)
 
    def __repr__(self):
        return '<student %r>' % (self.id)
    
class course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    cid = Column(String)
    cname = Column(String)
    de = Column(String)
    credit = Column(String)
    def __repr__(self):
        return '<course %r>' % (self.id)
    
class professor(Base):
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True, index=True)
    lid = Column(String(6), nullable=False)
    pfn = Column(String(10), nullable=False)
    pln = Column(String(10), nullable=False)
    pbirth = Column(String(10), nullable=False)
    pborncity = Column(String(150), nullable=False)
    paddress = Column(String(100), nullable=False)
    ppostalcode = Column(String(10), nullable=False)
    pcp = Column(String(11), nullable=False)
    php = Column(String(10), nullable=False)
    php_number = Column(String(10), nullable=False)
    pd = Column(String(50), nullable=False)
    pm = Column(String(50), nullable=False)
    pnid = Column(String(10), nullable=False)
    pscid = Column(String(150), nullable=False)

    def __repr__(self):
        return f'<professor id={self.id}>'
