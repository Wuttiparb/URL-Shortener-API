# ใช้ Python เป็นฐาน
FROM python:3.11-slim

# กำหนด working directory ใน container
WORKDIR /app

# copy requirements ก่อน แล้วค่อย install
# ทำแบบนี้เพื่อให้ Docker cache ได้ ไม่ต้อง install ใหม่ทุกครั้ง
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy โค้ดทั้งหมด
COPY . .

# บอกว่า container นี้เปิด port 8000
EXPOSE 8000

# คำสั่งรัน server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]