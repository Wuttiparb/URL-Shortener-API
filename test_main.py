import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

# สร้าง Database แยกสำหรับ test โดยเฉพาะ ไม่ยุ่งกับของจริง
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSession = sessionmaker(bind=engine)

# Override get_db ให้ใช้ test database แทน
def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ✅ case ปกติ — ย่อ URL สำเร็จ
def test_shorten_url():
    response = client.post("/shorten", json={
        "long_url": "https://www.youtube.com/watch?v=UyuWysU4v9g"
    })
    assert response.status_code == 200
    data = response.json()
    assert "short_id" in data        # ต้องมี short_id กลับมา
    assert data["clicks"] == 0       # คลิกเริ่มต้นต้องเป็น 0
    assert data["long_url"] == "https://www.youtube.com/watch?v=UyuWysU4v9g"


# ✅ case redirect — เปิด short URL แล้วต้องไปถูกที่
def test_redirect_url():
    # สร้าง short URL ก่อน
    res = client.post("/shorten", json={"long_url": "https://google.com"})
    short_id = res.json()["short_id"]

    # ทดสอบ redirect
    response = client.get(f"/{short_id}", follow_redirects=False)
    assert response.status_code == 307          # redirect status
    assert response.headers["location"] == "https://google.com"


# ✅ case นับคลิก — คลิกแล้วต้องเพิ่มขึ้น
def test_click_count():
    res = client.post("/shorten", json={"long_url": "https://google.com"})
    short_id = res.json()["short_id"]

    # คลิก 3 ครั้ง
    for _ in range(3):
        client.get(f"/{short_id}", follow_redirects=False)

    # เช็คสถิติ
    stats = client.get(f"/stats/{short_id}").json()
    assert stats["clicks"] == 3


# ❌ case URL ไม่เจอ — ต้องได้ 404
def test_url_not_found():
    response = client.get("/xxxxxx")
    assert response.status_code == 404


# ❌ case ดู stats URL ไม่เจอ — ต้องได้ 404
def test_stats_not_found():
    response = client.get("/stats/xxxxxx")
    assert response.status_code == 404

# สร้างและลบตารางทุกครั้งที่รัน test
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)