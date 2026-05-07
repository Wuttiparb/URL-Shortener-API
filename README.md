# URL Shortener API

API สำหรับย่อ URL พร้อมระบบนับจำนวนคลิก

## เทคโนโลยีที่ใช้
- Python + FastAPI
- SQLite / SQLAlchemy
- Docker
- pytest

## วิธีรัน

### ด้วย Docker
docker build -t url-shortener .
docker run -p 8000:8000 url-shortener

### รันตรงๆ
pip install -r requirements.txt
uvicorn main:app --reload

## API Endpoints
| Method | Endpoint | คำอธิบาย |
|--------|----------|----------|
| POST | /shorten | ย่อ URL |
| GET | /{short_id} | redirect ไป URL จริง |
| GET | /stats/{short_id} | ดูสถิติคลิก |

## รัน Test
pytest -v