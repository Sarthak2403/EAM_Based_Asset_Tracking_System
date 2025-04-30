import geopandas as gpd
import pandas as pd
import os

DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "infrastructure_assets.csv")

# Load relevant shapefiles
buildings = gpd.read_file(os.path.join(DATA_DIR, "gis_osm_buildings_a_free_1.shp"))
pois = gpd.read_file(os.path.join(DATA_DIR, "gis_osm_pois_free_1.shp"))
water = gpd.read_file(os.path.join(DATA_DIR, "gis_osm_water_a_free_1.shp"))
railways = gpd.read_file(os.path.join(DATA_DIR, "gis_osm_railways_free_1.shp"))

# Filter by relevant infrastructure asset types
building_assets = buildings[buildings['fclass'].isin(['train_station', 'public_building', 'school', 'hospital'])]
poi_assets = pois[pois['fclass'].isin(['water_tower', 'power_station', 'substation'])]
rail_assets = railways[railways['fclass'].isin(['rail', 'station'])]

# Combine all into one GeoDataFrame
combined = gpd.GeoDataFrame(pd.concat([building_assets, poi_assets, rail_assets], ignore_index=True))

# Assign asset_id
combined['asset_id'] = ["AST" + str(i).zfill(4) for i in range(1, len(combined) + 1)]
combined['asset_type'] = combined['fclass']
combined['location'] = combined['name'].fillna("Unknown")
combined['geometry'] = combined['geometry'].centroid
combined['latitude'] = combined.geometry.y
combined['longitude'] = combined.geometry.x

# Select and rename relevant columns
final_df = combined[['asset_id', 'asset_type', 'location', 'latitude', 'longitude']]
final_df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Extracted asset dataset saved to {OUTPUT_FILE}")