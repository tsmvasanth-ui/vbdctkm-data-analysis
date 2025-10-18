import streamlit as st
import gspread
import pandas as pd
import json
import os
import time
from google.oauth2.service_account import Credentials
import plotly.express as px

# ---------------------------
# 1. Streamlit Configuration
# ---------------------------
st.set_page_config(
    page_title="📊 VBDC TKM Data Dashboard",
    page_icon="🧬",
    layout="wide",
)

st.markdown(
    """
    <style>
        .main {
            background-color: #f9fafc;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        h1, h2, h3 {
            color: #1E88E5;
        }
        .stDataFrame {
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# 2. Google Sheet Connection
# ---------------------------
st.sidebar.title("⚙️ Settings")

# Load credentials
creds_json = os.getenv("GGOOGLE_CREDS")
creds_dict = json.loads(creds_json)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
gc = gspread.authorize(creds)

SPREADSHEET_ID = "1efD5IUpzCSGAU1zmSi6uqIzqXNGCyyJyKPLQBIyOulw"  # Your sheet ID

# ---------------------------
# 3. Data Loading Function
# ---------------------------
@st.cache_data(ttl=300)  # Auto-refresh every 5 minutes
def load_data():
    sheet = gc.open_by_key(SPREADSHEET_ID).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ---------------------------
# 4. Sidebar Filters
# ---------------------------
if not df.empty:
    st.sidebar.header("🔍 Filter Options")
    selected_column = st.sidebar.selectbox("Filter by column", df.columns)
    unique_values = df[selected_column].unique()
    selected_value = st.sidebar.selectbox("Select value", unique_values)
    filtered_df = df[df[selected_column] == selected_value]
else:
    filtered_df = pd.DataFrame()

# ---------------------------
# 5. Dashboard Layout
# ---------------------------
st.title("🩺 VBDC TKM - Data Analysis Dashboard")
st.caption("Live data synced from Google Sheets")

# Summary statistics
if not filtered_df.empty:
    st.subheader("📈 Key Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(filtered_df))
    with col2:
        st.metric("Unique Values", filtered_df[selected_column].nunique())
    with col3:
        st.metric("Missing Values", filtered_df.isna().sum().sum())
else:
    st.info("No data to display for the selected filter.")

# ---------------------------
# 6. Data Table
# ---------------------------
st.subheader("🧾 Filtered Data")
st.dataframe(filtered_df, use_container_width=True, height=400)

# ---------------------------
# 7. Charts & Comparisons
# ---------------------------
if not filtered_df.empty:
    st.subheader("📊 Data Visualization")

    # Choose chart type
    chart_type = st.selectbox("Select Chart Type", ["Bar", "Line", "Pie", "Scatter"])

    col_x = st.selectbox("Select X-axis", df.columns)
    col_y = st.selectbox("Select Y-axis (for numeric values)", df.columns)

    try:
        if chart_type == "Bar":
            fig = px.bar(filtered_df, x=col_x, y=col_y, color=col_x, title="Bar Chart")
        elif chart_type == "Line":
            fig = px.line(filtered_df, x=col_x, y=col_y, title="Line Chart")
        elif chart_type == "Pie":
            fig = px.pie(filtered_df, names=col_x, values=col_y, title="Pie Chart")
        elif chart_type == "Scatter":
            fig = px.scatter(filtered_df, x=col_x, y=col_y, color=col_x, title="Scatter Plot")

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Chart error: {e}")

# ---------------------------
# 8. Footer
# ---------------------------
st.markdown("---")
st.markdown("**Developed by Keerthi 🧠 | Powered by Google Sheets + Streamlit**")
