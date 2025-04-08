import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="Hourly Data Aggregation", layout="wide")
st.title("Hourly Maximum Values from SQLite Database")

def get_db_connection():
    conn = sqlite3.connect('crabs.db')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_aggregated_data(hours_to_display=24):
    conn = get_db_connection()
    
    # Calculate the cutoff time based on how many hours we want to display
    cutoff_time = datetime.now() - timedelta(hours=hours_to_display)
    
    try:
        query = """
        SELECT date, number 
        FROM crabs 
        WHERE date >= ?
        ORDER BY date
        """
        df = pd.read_sql_query(query, conn, params=(cutoff_time,))
        
        if df.empty:
            return None
        
        df['date'] = pd.to_datetime(df['date'])
        
        # Aggregate by hour, taking the max value
        df.set_index('date', inplace=True)
        hourly_df = df.resample('H').max().reset_index()
        conn.close()
        return hourly_df
    
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        conn.close()
        return None

# Sidebar controls
st.sidebar.header("Display Options")
hours_to_display = st.sidebar.slider(
    "Number of hours to display", 
    min_value=1, 
    max_value=168,
    value=24
)

refresh = st.sidebar.button("Refresh Data")

if refresh or True:  # Always load data initially
    data = fetch_aggregated_data(hours_to_display)
    
    if data is not None and not data.empty:
        st.subheader(f"Hourly Maximum Values (Last {hours_to_display} Hours)")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(data['date'], data['number'], marker='o', linestyle='-')
        ax.set_xlabel("Hour")
        ax.set_ylabel("Maximum Value")
        ax.set_title("Hourly Maximum of crabs Over Time")
        ax.grid(True)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Show raw data in an expander
        with st.expander("Show Raw Aggregated Data"):
            st.dataframe(data)
    else:
        st.warning("No data available for the selected time range.")

st.sidebar.markdown("""
### About this app
- Reads the number of crabs logged every 5 minutes from a database
- Aggregates values by hour (max)
- Displays results in an interactive chart
""")