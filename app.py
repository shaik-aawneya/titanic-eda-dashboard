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

# Interactive filters
st.sidebar.subheader("Filter Passengers")

gender_options = ["All"] + sorted(data["sex"].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", gender_options)

class_options = sorted(data["pclass"].dropna().unique().tolist())
selected_class = st.sidebar.multiselect(
    "Passenger Class",
    class_options,
    default=class_options
)

min_age = int(data["age"].min())
max_age = int(data["age"].max())

age_range = st.sidebar.slider(
    "Age Range",
    min_age,
    max_age,
    (min_age, max_age)
)

# Apply filters
filtered_data = data.copy()

if selected_gender != "All":
    filtered_data = filtered_data[
        filtered_data["sex"] == selected_gender
    ]

filtered_data = filtered_data[
    (filtered_data["pclass"].isin(selected_class)) &
    (filtered_data["age"].between(age_range[0], age_range[1]))
]

# Key metrics
st.subheader("Passenger Overview")

if not filtered_data.empty:
    total_passengers = len(filtered_data)
    survival_rate = filtered_data["survived"].mean() * 100
    average_age = filtered_data["age"].mean()
    average_fare = filtered_data["fare"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Passengers", f"{total_passengers:,}")
    col2.metric("Survival Rate", f"{survival_rate:.1f}%")
    col3.metric("Average Age", f"{average_age:.1f} years")
    col4.metric("Average Fare", f"${average_fare:.2f}")

else:
    st.warning("No passengers match the selected filters.")
