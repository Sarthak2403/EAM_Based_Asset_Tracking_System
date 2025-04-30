import streamlit as st
import pandas as pd
import sqlite3
import os
import pydeck as pdk

DB_PATH = os.path.join("database", "eam_assets.db")

# Load data
@st.cache_data
def load_assets():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM assets", conn)
    conn.close()
    return df

df = load_assets()

# --- Sidebar Filters ---
st.sidebar.title("🔍 Filter Assets")
phases = st.sidebar.multiselect("Select Phase(s)", options=df['phase'].unique(), default=df['phase'].unique())
projects = st.sidebar.multiselect("Select Project(s)", options=df['project_code'].unique(), default=df['project_code'].unique())
types = st.sidebar.multiselect("Select Asset Type(s)", options=df['asset_type'].unique(), default=df['asset_type'].unique())

# --- Apply Filters ---
filtered = df[
    (df['phase'].isin(phases)) &
    (df['project_code'].isin(projects)) &
    (df['asset_type'].isin(types))
]

# --- Title ---
st.title("🏗️ EAM Asset Tracking Dashboard")

# --- Metrics ---
st.metric("Total Assets", len(filtered))
st.metric("Distinct Asset Types", filtered['asset_type'].nunique())
st.metric("Projects Tracked", filtered['project_code'].nunique())

# --- Data Table ---
st.subheader("📋 Asset List")
st.dataframe(filtered)

# --- Map ---
if 'latitude' in df.columns and 'longitude' in df.columns:
    st.subheader("📍 Asset Map View")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=filtered['latitude'].mean(),
            longitude=filtered['longitude'].mean(),
            zoom=5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=filtered,
                get_position='[longitude, latitude]',
                get_radius=5000,
                get_color='[200, 30, 0, 160]',
                pickable=True,
            ),
        ],
    ))

# --- Export CSV ---
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered Data", csv, "filtered_assets.csv", "text/csv")

