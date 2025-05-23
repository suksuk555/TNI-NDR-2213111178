import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# ------------------ หน้าเว็บเบื้องต้น ------------------
st.set_page_config(page_title="SCB Stock Trend", layout="wide")

st.markdown("""
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
        }
        .subtitle {
            font-size: 18px;
            color: #808080;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📈 SCB Stock Closing Price Trend</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">ดูแนวโน้มราคาหุ้น SCB ด้วยกราฟเส้นจากข้อมูลราคาปิด พร้อมวิเคราะห์เทรนด์ด้วย Linear Regression</div><br>', unsafe_allow_html=True)

# ------------------ โหลดและเตรียมข้อมูล ------------------
df = pd.read_excel("stock_test2.xlsx")

def convert_thai_date(thai_date_str):
    from datetime import datetime
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

# ------------------ Linear Regression ------------------
X = df_sorted["วันที่"].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
y = df_sorted["ราคาปิด"].values
model = LinearRegression()
model.fit(X, y)
trend = model.predict(X)

# ------------------ สร้างกราฟ ------------------
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_sorted["วันที่"], y, label="Actual Closing Price", marker='o')
ax.plot(df_sorted["วันที่"], trend, label="Trend (Linear Regression)", linestyle="--", color="red")
ax.set_title("SCB Closing Price Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Closing Price (Baht)")
ax.legend()
ax.grid(True)

# ------------------ แสดงกราฟใน Streamlit ------------------
st.pyplot(fig)

# ------------------ แสดงตารางข้อมูลแบบสวย ------------------
with st.expander("📊 ดูข้อมูลราคาปิดแบบตาราง"):
    df_display = df_sorted.copy()
    df_display["วันที่"] = df_display["วันที่"].dt.strftime("%Y-%m-%d")
    df_display = df_display.round(2)
    st.dataframe(df_display)


st.markdown("สามารถดูข้อมูลหุ้น SCB ได้ที่ [https://www.settrade.com/th/equities/quote/SCB/historical-trading](https://www.settrade.com/th/equities/quote/SCB/historical-trading)")


# ------------------ ลายเซ็น ------------------
st.markdown("<br><hr><div style='text-align:center; font-size:16px;'>สุทธิชัย มุกโชควัฒนา 2213111178</div>", unsafe_allow_html=True)
