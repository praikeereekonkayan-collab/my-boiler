import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Condensate Dashboard",
    layout="wide",
    page_icon="💧",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Prompt', sans-serif;
    }
    
    .main {
        padding: 0px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    
    h1 {
        color: #1f3a93;
        text-align: center;
        margin-bottom: 30px;
    }
    
    h2 {
        color: #667eea;
        margin-top: 30px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("💧 ระบบติดตามข้อมูลน้ำควบแน่น (Condensate Monitoring System)")

# Sidebar
st.sidebar.title("⚙️ ตั้งค่า (Settings)")
st.sidebar.markdown("---")

# Load data
condensate_file = 'condensate_data.xlsx'

@st.cache_data
def load_condensate_data():
    if os.path.exists(condensate_file):
        try:
            df = pd.read_excel(condensate_file, sheet_name='%condensate')
            df['วันที่'] = pd.to_datetime(df['วันที่'])
            return df
        except Exception as e:
            st.error(f"ข้อผิดพลาดในการโหลดข้อมูล: {e}")
            return None
    else:
        st.error(f"ไม่พบไฟล์: {condensate_file}")
        return None

df = load_condensate_data()

if df is not None:
    # Sidebar filters
    st.sidebar.subheader("🔍 ตัวกรองข้อมูล")
    
    date_range = st.sidebar.date_input(
        "เลือกช่วงวันที่",
        value=(df['วันที่'].min().date(), df['วันที่'].max().date()),
        key="date_range"
    )
    
    status_filter = st.sidebar.multiselect(
        "เลือกสถานะ",
        options=['ปกติ', 'ผิดปกติ'],
        default=['ปกติ', 'ผิดปกติ'],
        key="status_filter"
    )
    
    # Filter data
    mask = (df['วันที่'].dt.date >= date_range[0]) & (df['วันที่'].dt.date <= date_range[1])
    mask = mask & (df['หมายเหตุ'].isin(status_filter))
    filtered_df = df[mask].copy()
    
    # KPI Section
    st.markdown("### 📊 ข้อมูลสำคัญ (Key Metrics)")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_condensate = filtered_df['ปริมาณน้ำควบแน่น (ลิตร)'].sum()
        st.metric(
            label="ปริมาณรวม (ลิตร)",
            value=f"{total_condensate:.0f}",
            delta=f"{total_condensate/len(filtered_df) if len(filtered_df) > 0 else 0:.0f} เฉลี่ยต่อวัน"
        )
    
    with col2:
        avg_temp = filtered_df['อุณหภูมิ (°C)'].mean()
        st.metric(
            label="อุณหภูมิเฉลี่ย",
            value=f"{avg_temp:.1f}°C"
        )
    
    with col3:
        avg_pressure = filtered_df['ความดัน (bar)'].mean()
        st.metric(
            label="ความดันเฉลี่ย",
            value=f"{avg_pressure:.2f} bar"
        )
    
    with col4:
        avg_tds = filtered_df['คุณภาพน้ำ (TDS)'].mean()
        st.metric(
            label="TDS เฉลี่ย",
            value=f"{avg_tds:.0f} ppm"
        )
    
    with col5:
        abnormal_count = len(filtered_df[filtered_df['หมายเหตุ'] == 'ผิดปกติ'])
        st.metric(
            label="เหตุการณ์ผิดปกติ",
            value=abnormal_count,
            delta=f"{(abnormal_count/len(filtered_df)*100 if len(filtered_df) > 0 else 0):.1f}%"
        )
    
    st.markdown("---")
    
    # Charts Section
    st.markdown("### 📈 กราฟแสดงข้อมูล")
    
    # Row 1: Line chart for volume over time
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("ปริมาณน้ำควบแน่นตามเวลา")
        fig_volume = go.Figure()
        fig_volume.add_trace(go.Scatter(
            x=filtered_df['วันที่'],
            y=filtered_df['ปริมาณน้ำควบแน่น (ลิตร)'],
            mode='lines+markers',
            name='ปริมาณน้ำ',
            line=dict(color='#667eea', width=2),
            marker=dict(size=8)
        ))
        fig_volume.update_layout(
            hovermode='x unified',
            height=400,
            template='plotly_white',
            yaxis_title="ปริมาณ (ลิตร)",
            xaxis_title="วันที่"
        )
        st.plotly_chart(fig_volume, use_container_width=True)
    
    with col2:
        st.subheader("อุณหภูมิและความดันตามเวลา")
        fig_temp_pressure = go.Figure()
        fig_temp_pressure.add_trace(go.Scatter(
            x=filtered_df['วันที่'],
            y=filtered_df['อุณหภูมิ (°C)'],
            mode='lines+markers',
            name='อุณหภูมิ (°C)',
            line=dict(color='#f56565', width=2),
            yaxis='y'
        ))
        fig_temp_pressure.add_trace(go.Scatter(
            x=filtered_df['วันที่'],
            y=filtered_df['ความดัน (bar)'],
            mode='lines+markers',
            name='ความดัน (bar)',
            line=dict(color='#48bb78', width=2),
            yaxis='y2'
        ))
        fig_temp_pressure.update_layout(
            hovermode='x unified',
            height=400,
            template='plotly_white',
            yaxis=dict(title="อุณหภูมิ (°C)"),
            yaxis2=dict(title="ความดัน (bar)", overlaying='y', side='right'),
            xaxis_title="วันที่"
        )
        st.plotly_chart(fig_temp_pressure, use_container_width=True)
    
    # Row 2: TDS and Status
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("คุณภาพน้ำ (TDS)")
        fig_tds = go.Figure()
        fig_tds.add_trace(go.Scatter(
            x=filtered_df['วันที่'],
            y=filtered_df['คุณภาพน้ำ (TDS)'],
            mode='lines+markers',
            name='TDS (ppm)',
            line=dict(color='#ed8936', width=2),
            marker=dict(size=8),
            fill='tozeroy'
        ))
        fig_tds.update_layout(
            hovermode='x unified',
            height=400,
            template='plotly_white',
            yaxis_title="TDS (ppm)",
            xaxis_title="วันที่"
        )
        st.plotly_chart(fig_tds, use_container_width=True)
    
    with col2:
        st.subheader("สถานะการทำงาน")
        status_counts = filtered_df['หมายเหตุ'].value_counts()
        colors = {'ปกติ': '#48bb78', 'ผิดปกติ': '#f56565'}
        fig_status = go.Figure(data=[
            go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                marker=dict(colors=[colors.get(x, '#667eea') for x in status_counts.index]),
                textinfo='label+percent+value'
            )
        ])
        fig_status.update_layout(height=400)
        st.plotly_chart(fig_status, use_container_width=True)
    
    st.markdown("---")
    
    # Data Table
    st.markdown("### 📋 ตารางข้อมูลประจำวัน")
    
    # Reorder columns for better display
    display_df = filtered_df[['วันที่', 'เวลา', 'ปริมาณน้ำควบแน่น (ลิตร)', 
                              'อุณหภูมิ (°C)', 'ความดัน (bar)', 'คุณภาพน้ำ (TDS)', 'หมายเหตุ']].copy()
    display_df['วันที่'] = display_df['วันที่'].dt.strftime('%Y-%m-%d')
    
    # Show data with conditional formatting
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # Download button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 ดาวน์โหลด CSV",
            data=csv,
            file_name=f"condensate_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, sheet_name='ข้อมูลน้ำควบแน่น', index=False)
        st.download_button(
            label="📥 ดาวน์โหลด Excel",
            data=buffer.getvalue(),
            file_name=f"condensate_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        st.info(f"📊 จำนวนรายการ: {len(filtered_df)} รายการ")

else:
    st.warning("⚠️ ไม่สามารถโหลดข้อมูลได้ โปรดตรวจสอบไฟล์")
