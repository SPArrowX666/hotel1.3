import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import seaborn as sns
import re
import numpy as np
import traceback

plt.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['axes.unicode_minus'] = False

try:
    df = pd.read_csv("hotelEn.csv")

    def extract_score(text):
        match = re.search(r'(\d\.\d+)', str(text))
        return float(match.group(1)) if match else np.nan

    def extract_discount(text):
        match = re.search(r'(\d+)%', str(text))
        return int(match.group(1)) if match else 0

    def extract_price(text):
        match = re.search(r'¥(\d{1,3}(,\d{3})*)', str(text))
        if match:
            price_str = match.group(1).replace(',', '')
            return int(price_str)
        return np.nan

    df["Score"] = df["Rating & Reviews"].apply(extract_score)
    df["Discount (%)"] = df["Discount"].apply(extract_discount)
    df["Price (Yen)"] = df["Price (Tax Included)"].apply(extract_price)
    hotel_names = df["Hotel Name"]

    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=df["Score"], y=hotel_names, palette="coolwarm", ax=ax)
    ax.set(title="Score by Hotel", xlabel="Score", ylabel="Hotel Name")
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    st.pyplot(fig)

    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=df["Discount (%)"], y=hotel_names, palette="YlGnBu", ax=ax)
    ax.set(title="Discount Rate (%) by Hotel", xlabel="Discount Rate (%)", ylabel="Hotel Name")
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    st.pyplot(fig)

    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=df["Price (Yen)"], y=hotel_names, palette="OrRd", ax=ax)
    ax.set(title="Minimum Price (Yen) by Hotel", xlabel="Price (Yen)", ylabel="Hotel Name")
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    st.pyplot(fig)

except Exception:
    st.error(f"Error occurred:\n{traceback.format_exc()}")
