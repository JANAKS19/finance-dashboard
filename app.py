import streamlit as st
import pandas as pd
import tempfile

from src.analytics import (
    filter_by_date,
    summary_metrics,
    daily_time_series
)
#comment

from src.charts import (
    income_pie_chart,
    expense_pie_chart,
    time_series_chart
)

from src.data_cleaning import clean_bank_data_from_excel


st.set_page_config(page_title="Finance Dashboard", layout="wide")
st.title("📊 Finance Management Dashboard")

# ==============================
# Upload Excel
# ==============================
uploaded_file = st.file_uploader(
    "Upload Bank Statement (Excel)",
    type=["xlsx"]
)

if not uploaded_file:
    st.warning("Please upload an Excel file to continue.")
    st.stop()

# Save uploaded Excel temporarily
with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
    tmp.write(uploaded_file.read())
    excel_path = tmp.name

# Clean data directly from Excel
df = clean_bank_data_from_excel(excel_path)

# ==============================
# Date cleaning (SAFE)
# ==============================
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])

if df.empty:
    st.error("No valid transaction dates found in the uploaded file.")
    st.stop()

min_date = df['date'].min().date()
max_date = df['date'].max().date()

# ==============================
# Date Range Selector
# ==============================
start_date, end_date = st.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

df_filtered = filter_by_date(df, start_date, end_date)

# ==============================
# KPIs
# ==============================
income, expense, net = summary_metrics(df_filtered)

c1, c2, c3 = st.columns(3)
c1.metric("Total Income", f"₹{income:,.0f}")
c2.metric("Total Expense", f"₹{expense:,.0f}")
c3.metric("Net Income", f"₹{net:,.0f}")

st.divider()

# ==============================
# Pie Charts
# ==============================
col1, col2 = st.columns(2)

with col1:
    if df_filtered[df_filtered['type'] == 'income'].empty:
        st.info("No income data for selected date range.")
    else:
        st.plotly_chart(
            income_pie_chart(df_filtered),
            use_container_width=True
        )

with col2:
    if df_filtered[df_filtered['type'] == 'expense'].empty:
        st.info("No expense data for selected date range.")
    else:
        st.plotly_chart(
            expense_pie_chart(df_filtered),
            use_container_width=True
        )

# ==============================
# Time Series (CUMULATIVE NET)
# ==============================
daily_df = daily_time_series(df_filtered)

st.plotly_chart(
    time_series_chart(daily_df),
    use_container_width=True
)
