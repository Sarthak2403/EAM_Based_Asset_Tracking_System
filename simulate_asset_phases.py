import pandas as pd
import os
import random
from datetime import datetime, timedelta

INPUT_FILE = os.path.join("data", "infrastructure_assets.csv")
OUTPUT_FILE = os.path.join("data", "asset_registry_with_phases.csv")

# Load asset data
df = pd.read_csv(INPUT_FILE)

# Assign random project codes
projects = ['INFRA001', 'INFRA002', 'INFRA003']
df['project_code'] = [random.choice(projects) for _ in range(len(df))]

# Define phases and status options
phases = ['Design', 'Construction', 'Operation', 'Decommissioned']
status_map = {
    'Design': 'Planned',
    'Construction': 'Installed',
    'Operation': 'Active',
    'Decommissioned': 'Retired'
}
df['phase'] = [random.choices(phases, weights=[0.2, 0.3, 0.4, 0.1])[0] for _ in range(len(df))]
df['status'] = df['phase'].map(status_map)

# Generate phase dates
base_date = datetime(2024, 1, 1)

def random_date(start_offset):
    return base_date + timedelta(days=random.randint(start_offset, start_offset + 60))

df['design_date'] = [random_date(0).date() for _ in range(len(df))]
df['install_date'] = [
    design + timedelta(days=random.randint(30, 90)) if phase != 'Design' else None
    for design, phase in zip(df['design_date'], df['phase'])
]
df['last_updated'] = [
    install + timedelta(days=random.randint(30, 180)) if install else design
    for design, install in zip(df['design_date'], df['install_date'])
]

# Save
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Asset lifecycle data saved to: {OUTPUT_FILE}")
