@echo off
REM Script to run Condensate Dashboard

echo.
echo ========================================
echo    Condensate Monitoring Dashboard
echo ========================================
echo.

REM Check if condensate_data.xlsx exists
if not exist "condensate_data.xlsx" (
    echo [!] ไฟล์ condensate_data.xlsx ไม่พบ
    echo [*] กำลังสร้างข้อมูลตัวอย่าง...
    python create_condensate_data.py
)

echo.
echo [*] กำลังเรียกใช้ Dashboard...
echo [*] Dashboard จะเปิดในเบราว์เซอร์ที่ http://localhost:8501
echo.
echo กดปุ่ม Ctrl+C เพื่อหยุดการทำงาน
echo.

streamlit run dashboard.py

pause
