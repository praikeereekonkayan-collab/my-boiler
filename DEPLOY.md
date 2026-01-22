# 💧 Condensate Monitoring Dashboard

Dashboard ตรวจสอบน้ำควบแน่นแบบ Real-time

## วิธี Deploy ไป Streamlit Cloud

### ขั้นตอนที่ 1: สร้าง GitHub Repository
1. ไปที่ https://github.com/new
2. สร้าง repository ชื่อ `condensate-dashboard`
3. Clone ลงเครื่องของคุณ

### ขั้นตอนที่ 2: Push ไฟล์ขึ้น GitHub
```bash
cd /path/to/condensate-dashboard
git add .
git commit -m "Initial commit - Condensate Dashboard"
git push origin main
```

### ขั้นตอนที่ 3: Deploy ไป Streamlit Cloud
1. ไปที่ https://share.streamlit.io
2. Click "New app"
3. เลือก:
   - GitHub repository: `your-username/condensate-dashboard`
   - Branch: `main`
   - Main file path: `dashboard.py`
4. Click "Deploy"

### ✅ เสร็จแล้ว!
หลังจาก 1-2 นาที คุณจะได้ URL แบบนี้:
```
https://your-username-condensate-dashboard.streamlit.app
```

ส่งลิ้งค์นี้ให้เพื่อนเปิดในโทรศัพย์ได้เลย 🎉

---

## ต้องการแก้ข้อมูล?
แก้ไขไฟล์ `create_condensate_data.py` แล้ว commit + push ก็เสร็จ
Streamlit Cloud จะ auto-update ให้เอง

## หมายเหตุ
- ไม่ต้องใส่ `condensate_data.xlsx` ใน GitHub
- Dashboard จะ generate ข้อมูลใหม่ทุกครั้งที่รีโหลด
