import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

"""
Export Dashboard as HTML File
สร้าง Dashboard เป็นไฟล์ HTML ที่สามารถแชร์ได้
"""

def create_html_dashboard():
    """สร้าง HTML Dashboard จากข้อมูล Excel"""
    
    # อ่านข้อมูล
    condensate_file = 'condensate_data.xlsx'
    
    if not os.path.exists(condensate_file):
        print("❌ ไฟล์ condensate_data.xlsx ไม่พบ")
        return
    
    try:
        df = pd.read_excel(condensate_file, sheet_name='%condensate')
        df['วันที่'] = pd.to_datetime(df['วันที่'])
        
        print("✅ อ่านข้อมูลสำเร็จ")
    except Exception as e:
        print(f"❌ ข้อผิดพลาด: {e}")
        return
    
    # คำนวณ KPI
    total_volume = df['ปริมาณน้ำควบแน่น (ลิตร)'].sum()
    avg_volume = df['ปริมาณน้ำควบแน่น (ลิตร)'].mean()
    avg_temp = df['อุณหภูมิ (°C)'].mean()
    avg_pressure = df['ความดัน (bar)'].mean()
    avg_tds = df['คุณภาพน้ำ (TDS)'].mean()
    abnormal_count = len(df[df['หมายเหตุ'] == 'ผิดปกติ'])
    
    # สร้าง HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>💧 Condensate Monitoring Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            
            .header {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            }}
            
            .header h1 {{
                color: #1f3a93;
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            
            .header p {{
                color: #666;
                font-size: 1.1em;
            }}
            
            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .metric-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
                border-left: 5px solid #667eea;
            }}
            
            .metric-value {{
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
                margin: 10px 0;
            }}
            
            .metric-label {{
                color: #666;
                font-size: 0.9em;
                text-transform: uppercase;
            }}
            
            .charts {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .chart-container {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            
            .chart-title {{
                color: #1f3a93;
                margin-bottom: 15px;
                font-size: 1.3em;
                font-weight: bold;
            }}
            
            .data-table {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                overflow-x: auto;
            }}
            
            .data-table table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 0.9em;
            }}
            
            .data-table th {{
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
            }}
            
            .data-table td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }}
            
            .data-table tr:hover {{
                background: #f5f5f5;
            }}
            
            .footer {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                color: #666;
                margin-top: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            
            .status-normal {{
                color: #48bb78;
                font-weight: bold;
            }}
            
            .status-abnormal {{
                color: #f56565;
                font-weight: bold;
            }}
            
            @media (max-width: 768px) {{
                .metrics {{
                    grid-template-columns: 1fr;
                }}
                .charts {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💧 ระบบติดตามข้อมูลน้ำควบแน่น</h1>
                <p>Condensate Monitoring Dashboard</p>
                <p style="margin-top: 10px; font-size: 0.9em;">สร้างเมื่อ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-label">ปริมาณรวม</div>
                    <div class="metric-value">{total_volume:.0f}</div>
                    <div class="metric-label">ลิตร</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">ปริมาณเฉลี่ย</div>
                    <div class="metric-value">{avg_volume:.1f}</div>
                    <div class="metric-label">ลิตร/วัน</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">อุณหภูมิเฉลี่ย</div>
                    <div class="metric-value">{avg_temp:.1f}</div>
                    <div class="metric-label">°C</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">ความดันเฉลี่ย</div>
                    <div class="metric-value">{avg_pressure:.2f}</div>
                    <div class="metric-label">bar</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">TDS เฉลี่ย</div>
                    <div class="metric-value">{avg_tds:.0f}</div>
                    <div class="metric-label">ppm</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">เหตุการณ์ผิดปกติ</div>
                    <div class="metric-value">{abnormal_count}</div>
                    <div class="metric-label">บันทึก</div>
                </div>
            </div>
            
            <div class="charts">
                <div class="chart-container">
                    <div class="chart-title">📈 ปริมาณน้ำควบแน่นตามเวลา</div>
                    <div id="chart1"></div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">🌡️ อุณหภูมิและความดัน</div>
                    <div id="chart2"></div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">💧 คุณภาพน้ำ (TDS)</div>
                    <div id="chart3"></div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">✅ สถานะการทำงาน</div>
                    <div id="chart4"></div>
                </div>
            </div>
            
            <div class="data-table">
                <h2 style="margin-bottom: 15px; color: #1f3a93;">📋 ตารางข้อมูลสมบูรณ์</h2>
                <table>
                    <thead>
                        <tr>
                            <th>วันที่</th>
                            <th>เวลา</th>
                            <th>ปริมาณน้ำ (ลิตร)</th>
                            <th>อุณหภูมิ (°C)</th>
                            <th>ความดัน (bar)</th>
                            <th>TDS (ppm)</th>
                            <th>หมายเหตุ</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    # เพิ่มแถวข้อมูล
    for _, row in df.iterrows():
        status_class = 'status-normal' if row['หมายเหตุ'] == 'ปกติ' else 'status-abnormal'
        html_content += f"""
                        <tr>
                            <td>{row['วันที่'].strftime('%Y-%m-%d')}</td>
                            <td>{row['เวลา']}</td>
                            <td>{row['ปริมาณน้ำควบแน่น (ลิตร)']:.2f}</td>
                            <td>{row['อุณหภูมิ (°C)']:.1f}</td>
                            <td>{row['ความดัน (bar)']:.2f}</td>
                            <td>{row['คุณภาพน้ำ (TDS)']:.0f}</td>
                            <td class="{status_class}">{row['หมายเหตุ']}</td>
                        </tr>
"""
    
    html_content += """
                    </tbody>
                </table>
            </div>
            
            <div class="footer">
                <p>💧 ระบบติดตามข้อมูลน้ำควบแน่น | Condensate Monitoring System</p>
                <p style="margin-top: 10px; font-size: 0.9em;">ข้อมูลสร้าง HTML Dashboard เพื่อการแชร์และเก็บอ้างอิง</p>
            </div>
        </div>
        
        <script>
"""
    
    # Chart 1: ปริมาณน้ำ
    html_content += """
            var trace1 = {
                x: [""" + ", ".join([f"'{d.strftime('%Y-%m-%d')}'" for d in df['วันที่']]) + """],
                y: [""" + ", ".join([str(v) for v in df['ปริมาณน้ำควบแน่น (ลิตร)']]) + """],
                mode: 'lines+markers',
                name: 'ปริมาณน้ำ',
                line: {color: '#667eea', width: 2},
                marker: {size: 6}
            };
            var layout1 = {
                xaxis: {title: 'วันที่'},
                yaxis: {title: 'ปริมาณ (ลิตร)'},
                hovermode: 'x unified',
                margin: {l: 50, r: 50, t: 50, b: 50}
            };
            Plotly.newPlot('chart1', [trace1], layout1, {responsive: true});
"""
    
    # Chart 2: อุณหภูมิและความดัน
    html_content += """
            var trace2a = {
                x: [""" + ", ".join([f"'{d.strftime('%Y-%m-%d')}'" for d in df['วันที่']]) + """],
                y: [""" + ", ".join([str(v) for v in df['อุณหภูมิ (°C)']]) + """],
                mode: 'lines+markers',
                name: 'อุณหภูมิ (°C)',
                line: {color: '#f56565', width: 2},
                yaxis: 'y'
            };
            var trace2b = {
                x: [""" + ", ".join([f"'{d.strftime('%Y-%m-%d')}'" for d in df['วันที่']]) + """],
                y: [""" + ", ".join([str(v) for v in df['ความดัน (bar)']]) + """],
                mode: 'lines+markers',
                name: 'ความดัน (bar)',
                line: {color: '#48bb78', width: 2},
                yaxis: 'y2'
            };
            var layout2 = {
                xaxis: {title: 'วันที่'},
                yaxis: {title: 'อุณหภูมิ (°C)'},
                yaxis2: {title: 'ความดัน (bar)', overlaying: 'y', side: 'right'},
                hovermode: 'x unified',
                margin: {l: 50, r: 50, t: 50, b: 50}
            };
            Plotly.newPlot('chart2', [trace2a, trace2b], layout2, {responsive: true});
"""
    
    # Chart 3: TDS
    html_content += """
            var trace3 = {
                x: [""" + ", ".join([f"'{d.strftime('%Y-%m-%d')}'" for d in df['วันที่']]) + """],
                y: [""" + ", ".join([str(int(v)) for v in df['คุณภาพน้ำ (TDS)']]) + """],
                mode: 'lines+markers',
                name: 'TDS (ppm)',
                fill: 'tozeroy',
                line: {color: '#ed8936', width: 2},
                marker: {size: 6}
            };
            var layout3 = {
                xaxis: {title: 'วันที่'},
                yaxis: {title: 'TDS (ppm)'},
                hovermode: 'x unified',
                margin: {l: 50, r: 50, t: 50, b: 50}
            };
            Plotly.newPlot('chart3', [trace3], layout3, {responsive: true});
"""
    
    # Chart 4: สถานะ
    status_counts = df['หมายเหตุ'].value_counts()
    labels = list(status_counts.index)
    values = list(status_counts.values)
    colors_pie = ['#48bb78' if l == 'ปกติ' else '#f56565' for l in labels]
    
    html_content += f"""
            var trace4 = {{
                labels: {labels},
                values: {values},
                type: 'pie',
                marker: {{colors: {colors_pie}}},
                textinfo: 'label+percent+value'
            }};
            var layout4 = {{
                margin: {{l: 50, r: 50, t: 50, b: 50}}
            }};
            Plotly.newPlot('chart4', [trace4], layout4, {{responsive: true}});
        </script>
    </body>
    </html>
"""
    
    # บันทึกเป็น HTML
    output_file = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ สร้าง HTML Dashboard สำเร็จ!")
    print(f"📁 ไฟล์: {output_file}")
    print(f"📊 ข้อมูล: {len(df)} บันทึก")
    print(f"💾 ขนาด: {os.path.getsize(output_file) / 1024:.1f} KB")
    print(f"\n📌 วิธีใช้:")
    print(f"   1. เปิดไฟล์: {output_file}")
    print(f"   2. สามารถแชร์ไฟล์นี้ให้คนอื่นเปิดในเบราว์เซอร์")
    print(f"   3. ไม่ต้องติดตั้ง Streamlit")

if __name__ == "__main__":
    create_html_dashboard()
