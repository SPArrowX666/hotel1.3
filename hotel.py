import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import re
import numpy as np
import traceback

# 字体和负号设置，避免乱码
mpl.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['axes.unicode_minus'] = False

# 正则提取评分
def extract_score(text):
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return np.nan
    match = re.search(r'(\d+\.\d+)', str(text))
    return float(match.group(1)) if match else np.nan

# 正则提取折扣（百分比整数）
def extract_discount(text):
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return 0
    match = re.search(r'(\d+)%', str(text))
    return int(match.group(1)) if match else 0

# 正则提取价格（整数，去逗号）
def extract_price(text):
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return np.nan
    match = re.search(r'¥(\d{1,3}(?:,\d{3})*)', str(text))
    if match:
        price_str = match.group(1).replace(',', '')
        return int(price_str)
    return np.nan

try:
    st.title("Hotel Data Analysis")

    # 读csv
    df = pd.read_csv("hotelEn.csv")

    st.subheader("Original Data Sample")
    st.write(df.head(10))

    # 提取数据列
    df["Score"] = df["Rating & Reviews"].apply(extract_score)
    df["Discount (%)"] = df["Discount"].apply(extract_discount)
    df["Price (Yen)"] = df["Price (Tax Included)"].apply(extract_price)

    st.subheader("Extracted Score, Discount, Price")
    st.write(df[["Hotel Name", "Score", "Discount (%)", "Price (Yen)"]].head(10))

    hotel_names = df["Hotel Name"]

    # 评分图表
    if df["Score"].dropna().empty:
        st.warning("Warning: No valid Score data found!")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=df["Score"], y=hotel_names, palette="coolwarm", ax=ax)
        ax.set(title="Score by Hotel", xlabel="Score", ylabel="Hotel Name")
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        st.pyplot(fig)

    # 折扣图表
    if df["Discount (%)"].sum() == 0:
        st.warning("Warning: No valid Discount data found!")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=df["Discount (%)"], y=hotel_names, palette="YlGnBu", ax=ax)
        ax.set(title="Discount Rate (%) by Hotel", xlabel="Discount Rate (%)", ylabel="Hotel Name")
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        st.pyplot(fig)

    # 价格图表
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
    st.error("Error occurred:\n" + traceback.format_exc())
