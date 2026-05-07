from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "sqlite:///./urls.db"  # ใช้ SQLite ก่อน ง่ายที่สุด

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ฟังก์ชันสำหรับเปิด/ปิด database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()