# This creates the page for displaying data visualizations.

import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
import json
import matplotlib.pyplot as plt

with open("data.json", "r") as file:
    data = json.load(file)

train_names = []
train_speeds = []

for item in data["data_points"]:
    train_names.append(item["label"])
    train_speeds.append(item["value"])

fig, ax = plt.subplots()
ax.bar(train_names, train_speeds, color="navy")

ax.set_title(data["chart_title"])
ax.set_xlabel("Train Name")
ax.set_ylabel("Maximum Operating Speed (km/h)")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)

st.subheader("Explore Train Speeds")

if "selected_trains" not in st.session_state:
    st.session_state.selected_trains = [
        item["label"] for item in data["data_points"]
    ]

selected_trains = st.multiselect(
    "Choose trains to compare:",
    [item["label"] for item in data["data_points"]],
    key="selected_trains"
)

dynamic_names = []
dynamic_speeds = []

for item in data["data_points"]:
    if item["label"] in st.session_state.selected_trains:
        dynamic_names.append(item["label"])
        dynamic_speeds.append(item["value"])

fig2, ax2 = plt.subplots()
ax2.plot(dynamic_names, dynamic_speeds, marker="o", color="darkorange")

ax2.set_title("Selected Trains: Operating Speeds")
ax2.set_xlabel("Train Name")
ax2.set_ylabel("Maximum Operating Speed (km/h)")

plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
fig2.tight_layout()

st.pyplot(fig2)



# PART 2: GRAPHS FROM data.csv

import pandas as pd

st.header("Student Lifestyle Survey")

# Read data from CSV file
survey_data = pd.read_csv("data.csv")

# Convert Value column to numeric
survey_data["Value"] = pd.to_numeric(
    survey_data["Value"],
    errors="coerce"
)

# Remove invalid rows
survey_data = survey_data.dropna(subset=["Category", "Value"])

# Calculate average hours for each category
average_data = survey_data.groupby("Category")["Value"].mean()

# STATIC VISUALIZATION

fig3, ax3 = plt.subplots()

ax3.bar(
    average_data.index,
    average_data.values,
    color="seagreen"
)

ax3.set_title("Average Daily Hours Spent on Activities")
ax3.set_xlabel("Activity")
ax3.set_ylabel("Average Hours per Day")

plt.tight_layout()

st.pyplot(fig3)

# DYNAMIC VISUALIZATION

st.subheader("Explore Student Lifestyle Data")

# Initialize Session State
if "selected_categories" not in st.session_state:
    st.session_state.selected_categories = (
        survey_data["Category"].unique().tolist()
    )

# Allow users to select activities
selected_categories = st.multiselect(
    "Choose activities to compare:",
    options=survey_data["Category"].unique().tolist(),
    key="selected_categories"
)

# Filter data based on selection
filtered_data = survey_data[
    survey_data["Category"].isin(selected_categories)
]

# Create scatter plot
fig4, ax4 = plt.subplots()

for position, category in enumerate(selected_categories):

    category_values = filtered_data[
        filtered_data["Category"] == category
    ]["Value"]

    ax4.scatter(
        [position] * len(category_values),
        category_values,
        label=category,
        s=100
    )

ax4.set_title("Student Responses: Daily Activity Hours")
ax4.set_xlabel("Activity")
ax4.set_ylabel("Hours per Day")
ax4.set_xticks(range(len(selected_categories)))
ax4.set_xticklabels(selected_categories)

if selected_categories:
    ax4.legend()

fig4.tight_layout()

st.pyplot(fig4)

# EXTRA CREDIT: SUMMARY STATISTICS

st.subheader("Summary Statistics")

selected_values = filtered_data["Value"].dropna()

if not selected_values.empty:

    mean_value = selected_values.mean()
    median_value = selected_values.median()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Mean Hours",
            value=f"{mean_value:.2f}"
        )

    with col2:
        st.metric(
            label="Median Hours",
            value=f"{median_value:.2f}"
        )

else:
    st.warning("Please select at least one activity.")
