from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class URL(Base):
    __tablename__ = "urls"

    id        = Column(Integer, primary_key=True)
    short_id  = Column(String, unique=True, index=True)  # รหัสสั้น เช่น "abc123"
    long_url  = Column(String)                           # URL ยาวจริงๆ
    clicks    = Column(Integer, default=0)               # นับจำนวนคลิก
    created_at = Column(DateTime, default=func.now())