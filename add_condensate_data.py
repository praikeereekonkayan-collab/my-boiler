import pandas as pd
from openpyxl import load_workbook
from datetime import datetime, timedelta
import random

"""
สคริปต์เพิ่มข้อมูลใหม่ลงในไฟล์ condensate_data.xlsx
"""

def add_new_condensate_data():
    file_path = 'condensate_data.xlsx'
    
    # โหลดข้อมูลเดิม
    df = pd.read_excel(file_path, sheet_name='%condensate')
    
    # สร้างข้อมูลใหม่
    last_date = pd.to_datetime(df['วันที่'].iloc[-1])
    new_dates = [(last_date + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(1, 8)]  # 7 วันต่อไป
    
    new_data = {
        'วันที่': new_dates,
        'เวลา': [f"{random.randint(0,23):02d}:{random.randint(0,59):02d}" for _ in new_dates],
        'ปริมาณน้ำควบแน่น (ลิตร)': [round(random.uniform(50, 500), 2) for _ in new_dates],
        'อุณหภูมิ (°C)': [round(random.uniform(60, 100), 1) for _ in new_dates],
        'ความดัน (bar)': [round(random.uniform(3, 8), 2) for _ in new_dates],
        'คุณภาพน้ำ (TDS)': [round(random.uniform(500, 2000), 0) for _ in new_dates],
        'หมายเหตุ': ['ปกติ' if random.random() > 0.15 else 'ผิดปกติ' for _ in new_dates]
    }
    
    new_df = pd.DataFrame(new_data)
    df = pd.concat([df, new_df], ignore_index=True)
    
    # บันทึกข้อมูลกลับไปที่ไฟล์
    df.to_excel(file_path, sheet_name='%condensate', index=False)
    print(f"✅ เพิ่มข้อมูล {len(new_df)} แถวลงในไฟล์เรียบร้อย")
    print(f"📊 ข้อมูลทั้งหมดในไฟล์: {len(df)} แถว")

if __name__ == "__main__":
    add_new_condensate_data()
