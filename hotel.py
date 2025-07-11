import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import re
import numpy as np
import traceback

# 设置字体和负号正常显示
mpl.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['axes.unicode_minus'] = False

# 改进版评分提取函数：用 re.search 全文匹配第一个浮点数
def extract_score(text):
    try:
        match = re.search(r'(\d+\.\d+)', str(text))
        return float(match.group(1)) if match else np.nan
    except:
        return np.nan

# 折扣提取函数，提取百分比数字，没有则返回0
def extract_discount(text):
    try:
        match = re.search(r'(\d+)%', str(text))
        return int(match.group(1)) if match else 0
    except:
        return 0

# 价格提取函数，匹配“¥”后数字，支持千分位逗号
def extract_price(text):
    try:
        match = re.search(r'¥(\d{1,3}(?:,\d{3})*)', str(text))
        if match:
            price_str = match.group(1).replace(',', '')
            return int(price_str)
        return np.nan
    except:
        return np.nan

try:
    # 读取CSV文件，注意路径是否正确
    df = pd.read_csv("hotelEn.csv")

    st.write("CSV columns:", df.columns.tolist())
    st.write("Sample data:", df.head())

    # 应用提取函数
    df["Score"] = df["Rating & Reviews"].apply(extract_score)
    df["Discount (%)"] = df["Discount"].apply(extract_discount)
    df["Price (Yen)"] = df["Price (Tax Included)"].apply(extract_price)

    # 输出提取结果预览，确认数据是否正确
    st.write("Extracted Score and Discount samples:")
    st.write(df[["Hotel Name", "Score", "Discount (%)", "Price (Yen)"]].head(10))

    hotel_names = df["Hotel Name"]

    # 根据数据有效性决定是否绘制图表
    if df["Score"].dropna().empty:
        st.warning("Warning: No valid Score data found!")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=df["Score"], y=hotel_names, palette="coolwarm", ax=ax)
        ax.set(title="Score by Hotel", xlabel="Score", ylabel="Hotel Name")
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        st.pyplot(fig)

    if df["Discount (%)"].sum() == 0:
        st.warning("Warning: No valid Discount data found!")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=df["Discount (%)"], y=hotel_names, palette="YlGnBu", ax=ax)
        ax.set(title="Discount Rate (%) by Hotel", xlabel="Discount Rate (%)", ylabel="Hotel Name")
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        st.pyplot(fig)

    if df["Price (Yen)"].dropna().empty:
        st.warning("Warning: No valid Price data found!")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=df["Price (Yen)"], y=hotel_names, palette="OrRd", ax=ax)
        ax.set(title="Minimum Price (Yen) by Hotel", xlabel="Price (Yen)", ylabel="Hotel Name")
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        st.pyplot(fig)

except Exception:
    st.error("An error occurred:\n" + traceback.format_exc())
