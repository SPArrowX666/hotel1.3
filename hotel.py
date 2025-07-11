import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import re
import numpy as np
import traceback

# 设置字体和负号显示
mpl.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['axes.unicode_minus'] = False

# 提取评分函数
def extract_score(text):
    try:
        match = re.match(r'(\d+\.\d+)', str(text))
        return float(match.group(1)) if match else np.nan
    except:
        return np.nan

# 提取折扣函数
def extract_discount(text):
    try:
        match = re.search(r'(\d+)%', str(text))
        return int(match.group(1)) if match else 0
    except:
        return 0

# 提取价格函数
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
    # 读取数据
    df = pd.read_csv("hotelEn.csv")

    # 显示表头确认加载成功
    st.write("CSV columns:", df.columns.tolist())
    st.write("CSV sample data:", df.head())

    # 应用提取函数
    df["Score"] = df["Rating & Reviews"].apply(extract_score)
    df["Discount (%)"] = df["Discount"].apply(extract_discount)
    df["Price (Yen)"] = df["Price (Tax Included)"].apply(extract_price)

    # 显示提取后的数据确认
    st.write("Parsed Score and Discount sample:")
    st.write(df[["Hotel Name", "Score", "Discount (%)", "Price (Yen)"]].head(10))

    hotel_names = df["Hotel Name"]

    # 判断数据是否有有效数值
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
