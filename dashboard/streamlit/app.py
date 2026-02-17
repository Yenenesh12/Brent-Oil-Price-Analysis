import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.data_loader import BrentDataLoader
from src.changepoint_model import BayesianChangePointModel

st.title("Brent Oil Price Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    data_path = project_root / 'data' / 'events' / 'BrentOilPrices.csv'
    loader = BrentDataLoader(data_path=str(data_path))
    df = loader.load_data()
    df = loader.preprocess()
    return df

df = load_data()

st.subheader("Price History")
st.line_chart(df.set_index("Date")["Price"])

# Change Point Detection
if st.button("Run Change Point Detection"):
    with st.spinner("Running Bayesian analysis... This may take a few minutes..."):
        data = df['Log_Returns'].dropna().values
        model = BayesianChangePointModel(data, n_changepoints=3)
        model.build_model()
        model.fit(draws=500, tune=500, chains=1, random_seed=42)
        fig = model.plot_results(dates=df['Date'].iloc[1:].values)
        st.pyplot(fig)
        st.success("Change point detection complete!")