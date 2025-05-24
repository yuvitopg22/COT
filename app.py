
import streamlit as st
import pandas as pd
import os

# Title
st.title("COT Positioning Dashboard")
st.markdown("View historical Net Positioning of Institutional and Retail Traders.")

# Load CSV files from the /data folder
data_folder = "data"
assets = [f.replace(".csv", "") for f in os.listdir(data_folder) if f.endswith(".csv")]
selected_asset = st.selectbox("Select Asset:", sorted(assets))

# Load selected asset CSV
file_path = os.path.join(data_folder, f"{selected_asset}.csv")
df = pd.read_csv(file_path)
df["Date"] = pd.to_datetime(df["Date"])
df.sort_values("Date", inplace=True)

# Date filter
min_date = df["Date"].min()
max_date = df["Date"].max()
date_range = st.slider("Select Date Range:", min_value=min_date, max_value=max_date, value=(min_date, max_date))
df_filtered = df[(df["Date"] >= date_range[0]) & (df["Date"] <= date_range[1])]

# Chart
st.subheader(f"Net Positioning for {selected_asset}")
st.line_chart(df_filtered.set_index("Date")[['Institutional Net', 'Retail Net']])

# Show raw data
if st.checkbox("Show raw data"):
    st.dataframe(df_filtered)

# Download CSV
csv_download = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered CSV", csv_download, f"{selected_asset}_filtered.csv", "text/csv")
