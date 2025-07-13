import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import numpy as np
import traceback


mpl.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['axes.unicode_minus'] = False

try:
    st.title("Hotel Data Analysis")

    df = pd.read_csv("hotelEn_cleaned.csv")

    st.subheader("Original Cleaned Data Sample")
    st.write(df.head(10))

    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Discount (%)"] = df["Discount"].str.replace('%', '').astype(float)
    df["Price (Yen)"] = pd.to_numeric(df["Price"], errors="coerce")

    st.subheader("Converted Rating, Discount, and Price")
    st.write(df[["Hotel Name", "Rating", "Discount (%)", "Price (Yen)"]].head(10))

    hotel_names = df["Hotel Name"]

    if df["Rating"].dropna().empty:
        st.warning("Warning: No valid Rating data found!")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=df["Rating"], y=hotel_names, palette="coolwarm", ax=ax)
        ax.set(title="Rating by Hotel", xlabel="Rating", ylabel="Hotel Name")
        st.pyplot(fig)

 
    if df["Discount (%)"].sum() == 0:
        st.warning("Warning: No valid Discount data found!")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=df["Discount (%)"], y=hotel_names, palette="YlGnBu", ax=ax)
        ax.set(title="Discount Rate (%) by Hotel", xlabel="Discount (%)", ylabel="Hotel Name")
        st.pyplot(fig)


    if df["Price (Yen)"].dropna().empty:
        st.warning("Warning: No valid Price data found!")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=df["Price (Yen)"], y=hotel_names, palette="OrRd", ax=ax)
        ax.set(title="Minimum Price (Yen) by Hotel", xlabel="Price (Yen)", ylabel="Hotel Name")
        st.pyplot(fig)

except Exception:
    st.error("Error occurred:\n" + traceback.format_exc())
