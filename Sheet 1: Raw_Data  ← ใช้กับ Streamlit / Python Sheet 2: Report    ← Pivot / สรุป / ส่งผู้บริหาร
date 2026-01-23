df = pd.read_excel(uploaded_file, header=None)

# ดึงเฉพาะแถวข้อมูลจริง
data = df.iloc[2:].copy()

data.columns = [
    "Date",
    "SoftMarkUp",
    "WaterMeter",
    "CondensateDiff",
    "Date2",
    "Target",
    "%Condensate",
    "Date3",
    "BHS",
    "Yueli",
    "Date4",
    "SteamTotal",
    "Date5",
    "AvgDiff",
    "Blank",
    "DiffLabel",
    "DiffValue"
]

data["Date"] = pd.to_datetime(data["Date"])
data["%Condensate"] = pd.to_numeric(data["%Condensate"], errors="coerce")

data = data.dropna(subset=["%Condensate"])
