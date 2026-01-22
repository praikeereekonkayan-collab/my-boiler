#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to run Condensate Monitoring Dashboard
ระบบเรียกใช้ Dashboard ติดตามน้ำควบแน่น
"""

import os
import sys
import subprocess
import platform

def check_file_exists(filename):
    """ตรวจสอบว่าไฟล์มีอยู่หรือไม่"""
    return os.path.exists(filename)

def main():
    print("\n" + "="*50)
    print("   💧 Condensate Monitoring Dashboard")
    print("="*50 + "\n")
    
    condensate_file = "condensate_data.xlsx"
    
    # ตรวจสอบไฟล์ข้อมูล
    if not check_file_exists(condensate_file):
        print(f"[!] ไฟล์ {condensate_file} ไม่พบ")
        print("[*] กำลังสร้างข้อมูลตัวอย่าง...")
        try:
            subprocess.run([sys.executable, "create_condensate_data.py"], check=True)
            print("[✓] สร้างข้อมูลสำเร็จ\n")
        except subprocess.CalledProcessError:
            print("[✗] ข้อผิดพลาดในการสร้างข้อมูล")
            return 1
    
    # เรียกใช้ Dashboard
    print("[*] กำลังเรียกใช้ Dashboard...")
    print("[*] Dashboard จะเปิดที่ http://localhost:8501")
    print("[*] กดปุ่ม Ctrl+C เพื่อหยุดการทำงาน\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\n\n[*] Dashboard ปิดแล้ว")
        return 0
    except Exception as e:
        print(f"\n[✗] ข้อผิดพลาด: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
