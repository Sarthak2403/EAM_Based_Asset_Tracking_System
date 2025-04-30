import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("database", "eam_assets.db")

# Connect to DB
conn = sqlite3.connect(DB_PATH)

# --- Query 1: Asset count by phase ---
print("📊 Assets by Phase:")
query = "SELECT phase, COUNT(*) as count FROM assets GROUP BY phase ORDER BY count DESC;"
print(pd.read_sql_query(query, conn), "\n")

# --- Query 2: Asset types per project ---
print("🏗️ Assets by Type and Project:")
query = """
SELECT project_code, asset_type, COUNT(*) as count
FROM assets
GROUP BY project_code, asset_type
ORDER BY project_code, count DESC;
"""
print(pd.read_sql_query(query, conn), "\n")

# --- Query 3: Recently installed assets (last 90 days) ---
print("📅 Recently Installed Assets:")
query = """
SELECT asset_id, asset_type, install_date
FROM assets
WHERE install_date >= DATE('now', '-90 days')
ORDER BY install_date DESC
LIMIT 10;
"""
print(pd.read_sql_query(query, conn), "\n")

# --- Query 4: Top 5 most common asset types ---
print("📌 Top 5 Asset Types:")
query = """
SELECT asset_type, COUNT(*) as count
FROM assets
GROUP BY asset_type
ORDER BY count DESC
LIMIT 5;
"""
print(pd.read_sql_query(query, conn), "\n")

conn.close()