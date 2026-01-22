import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Boiler Industrial Dashboard",
    layout="wide",
    page_icon="🏭"
)

st.markdown("## 🏭 Boiler Utility Dashboard")

# ===== SIDEBAR =====
st.sidebar.header("⚙️ ตัวกรอง")

uploaded_file = st.sidebar.file_uploader(
    "อัปโหลดไฟล์ Excel",
    type=["xlsx"]
)

target_return = st.sidebar.number_input(
    "Target Condensate Return (%)",
    value=70
)

# ===== LOAD DATA =====
if uploaded_file:
    df = pd.read_excel(uploaded_file)
else:
    st.info("ยังไม่อัปโหลดไฟล์ — ใช้ข้อมูลตัวอย่าง")

    df = pd.DataFrame({
        "Date": pd.date_range("2026-01-01", periods=10),
        "Steam": [120,130,125,140,150,148,145,160,155,150],
        "Condensate": [70,80,75,85,90,88,85,95,92,90]
    })

df["Return_%"] = df["Condensate"] / df["Steam"] * 100
df["Loss"] = df["Steam"] - df["Condensate"]

# ===== KPI =====
col1, col2, col3, col4 = st.columns(4)

col1.metric("🔥 Steam รวม", f"{df['Steam'].sum():,.0f}")
col2.metric("♻️ Condensate รวม", f"{df['Condensate'].sum():,.0f}")
col3.metric("📊 Return %", f"{df['Return_%'].mean():.1f} %")
col4.metric("💧 Water Loss", f"{df['Loss'].sum():,.0f}")

# ===== STATUS =====
if df["Return_%"].mean() >= target_return:
    st.success("✅ Condensate อยู่ในเกณฑ์")
else:
    st.error("🚨 Condensate ต่ำกว่า Target")

# ===== CHART =====
st.subheader("📈 แนวโน้ม")

colA, colB = st.columns(2)

with colA:
    st.line_chart(df.set_index("Date")[["Steam", "Condensate"]])

with colB:
    st.line_chart(df.set_index("Date")[["Return_%"]])

# ===== TABLE =====
st.subheader("📋 ตารางรายวัน")

def highlight(row):
    color = "background-color: #ffcccc" if row["Return_%"] < target_return else ""
    return [color]*len(row)

st.dataframe(
    df.style.apply(highlight, axis=1),
    use_container_width=True
)
