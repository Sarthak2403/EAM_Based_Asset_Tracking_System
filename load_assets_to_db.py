import sqlite3
import pandas as pd
import os

CSV_PATH = os.path.join("data", "asset_registry_with_phases.csv")
DB_PATH = os.path.join("database", "eam_assets.db")
TABLE_NAME = "assets"

# Ensure output folder exists
os.makedirs("database", exist_ok=True)

# Load the asset registry
df = pd.read_csv(CSV_PATH)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Write to SQL table (overwrite if exists)
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)

# Check table count
cursor = conn.cursor()
cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
count = cursor.fetchone()[0]

conn.close()
print(f"✅ Loaded {count} assets into '{DB_PATH}' → table '{TABLE_NAME}'")
