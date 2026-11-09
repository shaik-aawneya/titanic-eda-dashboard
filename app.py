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

# Exploratory Data Analysis
st.divider()
st.header("Survival Analysis")

if not filtered_data.empty:

    # Create age groups for analysis
    chart_data = filtered_data.copy()

    chart_data["age_group"] = pd.cut(
        chart_data["age"],
        bins=[0, 12, 18, 35, 60, 100],
        labels=["Child", "Teenager", "Young Adult", "Adult", "Senior"]
    )

    # Survival by gender
    st.subheader("1. Survival by Gender")

    gender_survival = (
        chart_data.groupby("sex", observed=False)["survived"]
        .mean().reset_index()
    )
    gender_survival["survived"] *= 100

    fig1 = px.bar(
        gender_survival,
        x="sex",
        y="survived",
        color="sex",
        text_auto=".1f",
        title="Survival Rate by Gender",
        labels={"sex": "Gender", "survived": "Survival Rate (%)"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Survival by passenger class
    st.subheader("2. Survival by Passenger Class")

    class_survival = (
        chart_data.groupby("pclass", observed=False)["survived"]
        .mean().reset_index()
    )
    class_survival["survived"] *= 100

    fig2 = px.bar(
        class_survival,
        x="pclass",
        y="survived",
        color="pclass",
        text_auto=".1f",
        title="Survival Rate by Passenger Class",
        labels={"pclass": "Passenger Class", "survived": "Survival Rate (%)"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Survival by age group
    st.subheader("3. Survival by Age Group")

    age_survival = (
        chart_data.groupby("age_group", observed=False)["survived"]
        .mean().reset_index()
    )
    age_survival["survived"] *= 100

    fig3 = px.bar(
        age_survival,
        x="age_group",
        y="survived",
        color="age_group",
        text_auto=".1f",
        title="Survival Rate by Age Group",
        labels={"age_group": "Age Group", "survived": "Survival Rate (%)"}
    )
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Select different filters to view the analysis.")
# Key Findings
st.divider()
st.header("Key Findings")

if not filtered_data.empty:

    gender_rates = (
        filtered_data.groupby("sex")["survived"].mean() * 100
    )

    class_rates = (
        filtered_data.groupby("pclass")["survived"].mean() * 100
    )

    if not gender_rates.empty:
        top_gender = gender_rates.idxmax()
        st.write(
            f"- **Gender:** {top_gender.title()} passengers "
            f"had the highest survival rate "
            f"({gender_rates.max():.1f}%)."
        )

    if not class_rates.empty:
        top_class = class_rates.idxmax()
        st.write(
            f"- **Passenger class:** Class {top_class} "
            f"had the highest survival rate "
            f"({class_rates.max():.1f}%)."
        )

    age_rates = (
        chart_data.groupby("age_group", observed=False)["survived"]
        .mean().dropna() * 100
    )

    if not age_rates.empty:
        top_age_group = age_rates.idxmax()
        st.write(
            f"- **Age group:** {top_age_group} passengers "
            f"had the highest survival rate "
            f"({age_rates.max():.1f}%)."
        )

# Limitations
st.divider()
st.header("Limitations")

st.markdown("""
- The analysis describes associations, not proof of causation.
- Some passenger information was missing in the original dataset.
- The results describe the passengers in this dataset and may not
  represent every person aboard the Titanic.
- Survival patterns may have been influenced by factors not included
  in this analysis.
""")

st.caption("Project: Titanic Exploratory Data Analysis | Python, Pandas, Streamlit and Plotly")
