
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="COT Dashboard", layout="wide")
st.title("COT Positioning Dashboard")
st.markdown("View historical Net Positioning of Institutional and Retail Traders.")

data_folder = "data"
if not os.path.exists(data_folder):
    st.error(f"Data folder '{data_folder}' not found.")
else:
    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
    assets = [f.replace(".csv", "") for f in csv_files]

    if not assets:
        st.warning("No CSV files found in the data folder.")
    else:
        selected_asset = st.selectbox("Select Asset:", sorted(assets))
        file_path = os.path.join(data_folder, f"{selected_asset}.csv")

        try:
            df = pd.read_csv(file_path)
            if df.empty:
                st.warning("The selected file is empty.")
            else:
                df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
                df = df.dropna(subset=["Date"])
                df.sort_values("Date", inplace=True)

                min_date = df["Date"].min()
                max_date = df["Date"].max()

                if pd.isnull(min_date) or pd.isnull(max_date):
                    st.warning("Invalid date values in this file.")
                else:
                    date_range = st.slider("Select Date Range:", min_value=min_date, max_value=max_date, value=(min_date, max_date))
                    df_filtered = df[(df["Date"] >= date_range[0]) & (df["Date"] <= date_range[1])]

                    st.subheader(f"Net Positioning for {selected_asset}")
                    st.line_chart(df_filtered.set_index("Date")[['Institutional Net', 'Retail Net']])

                    if st.checkbox("Show raw data"):
                        st.dataframe(df_filtered)

                    csv_download = df_filtered.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Filtered CSV", csv_download, f"{selected_asset}_filtered.csv", "text/csv")
        except Exception as e:
            st.error(f"Failed to load or process file: {e}")
