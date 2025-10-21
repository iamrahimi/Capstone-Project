import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ========================
# 1️ Connect to Database
# ========================
DB_NAME = "./db/mlb_history.db"

@st.cache_data
def load_table(table_name):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(f'SELECT * FROM "{table_name}"', conn)
    conn.close()
    return df


# ========================
# 2️  Load Data
# ========================
st.set_page_config(page_title="MLB History Dashboard", layout="wide")

st.title("Major League Baseball History Dashboard")

# Load tables dynamically
conn = sqlite3.connect(DB_NAME)
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)["name"].tolist()
conn.close()

if not tables:
    st.error("No tables found in the database.")
    st.stop()

# Let user pick which data to visualize
table_choice = st.selectbox(" Choose a data table:", tables)

data = load_table(table_choice)
st.write(f"### Data Preview: {table_choice}")
st.dataframe(data.head(10))

# ========================
# 3️  Filters (Interactive)
# ========================
numeric_cols = data.select_dtypes(include=["number", "float", "int"]).columns.tolist()
categorical_cols = data.select_dtypes(exclude=["number", "float", "int"]).columns.tolist()

if categorical_cols:
    cat_col = st.selectbox("🔹 Choose a category to filter:", categorical_cols)
    unique_vals = sorted(data[cat_col].dropna().unique())
    selected_vals = st.multiselect(f"Select {cat_col} values:", unique_vals, default=unique_vals[:3])
    data = data[data[cat_col].isin(selected_vals)]


# ========================
# 4️  Visualizations
# ========================
st.subheader(" Visualizations")

if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
    # Visualization 1: Bar Chart
    fig1 = px.bar(data, x=categorical_cols[0], y=numeric_cols[0],
                  title=f"{numeric_cols[0]} by {categorical_cols[0]}")
    st.plotly_chart(fig1, use_container_width=True)

if len(numeric_cols) >= 2:
    # Visualization 2: Scatter Plot
    fig2 = px.scatter(data, x=numeric_cols[0], y=numeric_cols[1],
                      color=categorical_cols[0] if categorical_cols else None,
                      title=f"Scatter Plot of {numeric_cols[0]} vs {numeric_cols[1]}")
    st.plotly_chart(fig2, use_container_width=True)

if len(numeric_cols) >= 1:
    # Visualization 3: Histogram
    fig3 = px.histogram(data, x=numeric_cols[0], nbins=10,
                        title=f"Distribution of {numeric_cols[0]}")
    st.plotly_chart(fig3, use_container_width=True)

st.success(" Dashboard loaded successfully!")