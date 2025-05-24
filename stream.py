import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

st.set_page_config(page_title="SCB Stock Trend", layout="wide")

st.markdown("""
    <style>
        .subtitle {
            font-size: 18px;
            color: #808080;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📈 SCB Stock Closing Price Trend")

st.markdown('<div class="subtitle">ดูแนวโน้มราคาหุ้น SCB โดยเป็นราคาย้อนหลังของหุ้น SCB 6 เดือน</div><br>', unsafe_allow_html=True)

df = pd.read_excel("stock_test2.xlsx")

def convert_thai_date(thai_date_str):
    thai_months = {
        "ม.ค.": "01", "ก.พ.": "02", "มี.ค.": "03", "เม.ย.": "04",
        "พ.ค.": "05", "มิ.ย.": "06", "ก.ค.": "07", "ส.ค.": "08",
        "ก.ย.": "09", "ต.ค.": "10", "พ.ย.": "11", "ธ.ค.": "12"
    }
    day, thai_month, buddhist_year = thai_date_str.strip().split()
    month = thai_months[thai_month]
    year = str(int(buddhist_year) - 543)
    date_str = f"{year}-{month}-{day}"
    return pd.to_datetime(date_str)

df["วันที่"] = df["วันที่"].apply(convert_thai_date)
df_sorted = df.sort_values("วันที่")

X = df_sorted["วันที่"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
y = df_sorted["ราคาปิด"].values
model = LinearRegression()
model.fit(X, y)
trend = model.predict(X)

col1, col2 = st.columns(2)

with col1:
    chart_type = st.selectbox(
        "📊 เลือกประเภทกราฟ",
        ("Line Chart",  "Pie Chart")
    )

with col2:
    fig_width = st.slider("📐 ปรับความกว้างของกราฟ (นิ้ว)", 8, 20, 12)
    fig_height = st.slider("📏 ปรับความสูงของกราฟ (นิ้ว)", 4, 12, 6)

fig, ax = plt.subplots(figsize=(fig_width, fig_height))

if chart_type == "Line Chart":
    ax.plot(df_sorted["วันที่"], y, label="Actual Closing Price", marker='o')
    ax.plot(df_sorted["วันที่"], trend, label="Trend (Linear Regression)", linestyle="--", color="red")
    ax.set_title("SCB Closing Price Trend (Line Chart)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price (Baht)")
    ax.legend()
    ax.grid(True)


elif chart_type == "Pie Chart":
    latest_df = df_sorted.tail(5)
    ax.pie(latest_df["ราคาปิด"], labels=latest_df["วันที่"].dt.strftime('%Y-%m-%d'), autopct='%1.1f%%')
    ax.set_title("Pie Chart of Last 5 Closing Prices")

#แสดงกราฟ
st.pyplot(fig)

#แสดงตารางข้อมูล 
with st.expander("📋 ดูข้อมูลราคาปิดแบบตาราง"):
    df_display = df_sorted.copy()
    df_display["วันที่"] = df_display["วันที่"].dt.strftime("%Y-%m-%d")
    df_display.index = range(1, len(df_display) + 1)

    # กำหนดให้ทุกคอลัมน์ที่เป็นตัวเลขแสดงทศนิยม 2 ตำแหน่ง
    st.dataframe(df_display.style.format({col: "{:.2f}" for col in df_display.select_dtypes(include='number').columns}))

st.markdown("🔗 ดูข้อมูลหุ้น SCB ได้ที่ [SETTRADE](https://www.settrade.com/th/equities/quote/SCB/historical-trading)")

st.markdown("<br><hr><div style='text-align:center; font-size:16px;'>สุทธิชัย มุกโชควัฒนา 2213111178</div>", unsafe_allow_html=True)
