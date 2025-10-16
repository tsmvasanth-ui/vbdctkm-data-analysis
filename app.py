import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ---------------------------
# 1. Service Account Setup
# ---------------------------
SERVICE_ACCOUNT_FILE = "vbdctkm-2c5de101d3c0.JSON"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)
gc = gspread.authorize(creds)

# ---------------------------
# 2. Spreadsheet Setup
# ---------------------------
SPREADSHEET_ID = "1efD5IUpzCSGAU1zmSi6uqIzqXNGCyyJyKPLQBIyOulw"  # replace with your sheet ID
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

# ---------------------------
# 3. Load data into Pandas
# ---------------------------
data = sheet.get_all_records()
df = pd.DataFrame(data)

# ---------------------------
# 4. Streamlit App
# ---------------------------
st.set_page_config(page_title="VBDC TKM Data Analysis", layout="wide")
st.title("📊 VBDC TKM 2025 - Data Analysis")

st.sidebar.header("Filter Options")

# Example: Filter by a column (replace 'Column1' with your actual column name)
if not df.empty:
    column_to_filter = st.sidebar.selectbox("Select column to filter", df.columns)
    unique_values = df[column_to_filter].unique()
    selected_value = st.sidebar.selectbox("Select value", unique_values)
    filtered_df = df[df[column_to_filter] == selected_value]
else:
    filtered_df = df

st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Example: Simple chart
st.subheader("Chart Example")
if not filtered_df.empty:
    chart_column = st.selectbox("Select column for chart", filtered_df.columns)
    st.bar_chart(filtered_df[chart_column])
