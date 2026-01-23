import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="% Condensate Analysis", layout="wide")

st.title("📊 % Condensate Boiler Analysis")

# โหลดไฟล์ Excel
uploaded_file = st.file_uploader("📂 อัปโหลดไฟล์ %CONDENSATE BOILER.xlsx", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("🔍 ข้อมูลดิบ")
    st.dataframe(df)

    # ถ้ายังไม่มี %Condensate ให้คำนวณ
    if "%Condensate" not in df.columns:
        df["%Condensate"] = (df["Condensate (kg)"] / df["Feed Water (kg)"]) * 100

    # เลือกช่วงวันที่
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        start_date = st.date_input("📅 วันที่เริ่ม", df["Date"].min())
        end_date = st.date_input("📅 วันที่สิ้นสุด", df["Date"].max())

        df = df[(df["Date"] >= pd.to_datetime(start_date)) &
                (df["Date"] <= pd.to_datetime(end_date))]

    st.subheader("📈 กราฟ % Condensate")

    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["%Condensate"], marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("% Condensate")
    ax.set_title("% Condensate Usage Trend")
    ax.grid(True)

    st.pyplot(fig)

    st.metric("ค่าเฉลี่ย %Condensate", f"{df['%Condensate'].mean():.2f} %")

else:
    st.info("⬆️ กรุณาอัปโหลดไฟล์ Excel เพื่อเริ่มวิเคราะห์")
