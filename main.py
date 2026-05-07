from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import random, string

from database import engine, get_db, Base
from models import URL
from schemas import URLCreate, URLResponse

# สร้างตารางใน database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ฟังก์ชันสร้างรหัสสั้น เช่น "aB3xK9"
def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


# POST /shorten — รับ URL ยาว แล้วคืน URL สั้น
@app.post("/shorten", response_model=URLResponse)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    short_id = generate_short_id()
    new_url = URL(short_id=short_id, long_url=payload.long_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url


# GET /{short_id} — เปิด URL สั้น แล้ว redirect ไป URL ยาว
@app.get("/{short_id}")
def redirect_url(short_id: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_id == short_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="ไม่พบ URL นี้")
    url.clicks += 1
    db.commit()
    return RedirectResponse(url.long_url)


# GET /stats/{short_id} — ดูสถิติว่ามีคนคลิกกี่ครั้ง
@app.get("/stats/{short_id}", response_model=URLResponse)
def get_stats(short_id: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_id == short_id).first()
    if not url:
        raise HTTPException(status_code=404, detail="ไม่พบ URL นี้")
    return url