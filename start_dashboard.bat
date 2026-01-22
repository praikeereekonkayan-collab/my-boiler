@echo off
chcp 65001 > nul
cd /d "C:\Users\nb.boiler\OneDrive\Desktop\test"
python -m streamlit run dashboard.py
pause
