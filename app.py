import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Titanic EDA Dashboard",
    page_icon="🚢",
    layout="wide"
)

# Dashboard title
st.title("🚢 Titanic Exploratory Data Analysis")
st.markdown(
    "An interactive analysis of passenger survival patterns "
    "using the Titanic dataset."
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("titanic_cleaned.csv")

data = load_data()

# Sidebar
st.sidebar.header("Dashboard Filters")

st.sidebar.write(
    "Explore passenger survival patterns using the filters."
)
