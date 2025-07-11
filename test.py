import streamlit as st
import pandas as pd
import re
import numpy as np

st.title("Hotel Data Debug")

@st.cache_data
def load_data():
    return pd.read_csv("hotelEn.csv")

df = load_data()

st.write("Raw Data Sample:")
st.write(df.head(5))

def extract_score(text):
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return np.nan
    m = re.search(r'(\d+\.\d+)', str(text))
    return float(m.group(1)) if m else np.nan

def extract_discount(text):
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return 0
    m = re.search(r'(\d+)%', str(text))
    return int(m.group(1)) if m else 0

def extract_price(text):
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return np.nan
    m = re.search(r'¥(\d{1,3}(?:,\d{3})*)', str(text))
    if m:
        return int(m.group(1).replace(',', ''))
    return np.nan

df["Score"] = df["Rating & Reviews"].apply(extract_score)
df["Discount (%)"] = df["Discount"].apply(extract_discount)
df["Price (Yen)"] = df["Price (Tax Included)"].apply(extract_price)

st.write("Extracted Data Sample:")
st.write(df[["Hotel Name", "Score", "Discount (%)", "Price (Yen)"]].head(10))

score_valid = df["Score"].dropna()
discount_valid = df["Discount (%)"].loc[df["Discount (%)"]>0]
price_valid = df["Price (Yen)"].dropna()

st.write(f"Valid Scores count: {len(score_valid)}")
st.write(f"Valid Discounts count: {len(discount_valid)}")
st.write(f"Valid Prices count: {len(price_valid)}")
