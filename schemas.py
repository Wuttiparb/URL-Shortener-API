from pydantic import BaseModel

# รูปแบบข้อมูลที่รับเข้ามา
class URLCreate(BaseModel):
    long_url: str

# รูปแบบข้อมูลที่ส่งกลับไป
class URLResponse(BaseModel):
    short_id: str
    long_url: str
    clicks: int

    class Config:
        from_attributes = True