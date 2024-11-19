
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
from pyproj import CRS
import matplotlib.pyplot as plt

# Load the Excel file
try:
    vessel = pd.read_excel("AIS_data_20220811.xlsx")
    print("Excel file successfully loaded.")
except FileNotFoundError:
    raise FileNotFoundError("The file 'AIS_data_20220811.xlsx' was not found.")

# Sort and handle missing values
vessel = vessel.sort_values("mmsi", ascending=True)
missing_values = vessel.isnull().sum()
print("Missing values statistics:\n", missing_values)

# Drop unnecessary columns
if {'vessel_type_main', 'vessel_type_sub'}.issubset(vessel.columns):
    vessel = vessel.drop(columns=['vessel_type_main', 'vessel_type_sub'], errors='ignore')

# Ensure necessary columns exist
required_columns = {'longitude', 'latitude', 'ts_pos_utc', 'mmsi'}
if not required_columns.issubset(vessel.columns):
    raise ValueError(f"Missing required columns: {required_columns - set(vessel.columns)}")

# Create geometry objects
geometry = [Point(xy) for xy in zip(vessel.longitude, vessel.latitude)]
crs = CRS("epsg:4326")

# Process time data and create GeoDataFrame
vessel['time_order'] = vessel['ts_pos_utc'].round(-6)
df = gpd.GeoDataFrame(vessel, crs=crs, geometry=geometry)

# Filter and group data
filtered = df.groupby('mmsi').filter(lambda x: len(x) > 5)
filtered = filtered.sort_values('ts_pos_utc', ascending=True)

# Function to generate LineString for track lines
def create_linestring(geometries):
    if len(geometries) > 1:
        return LineString(geometries.tolist())
    return None

# Generate track lines
track_lines = (
    filtered.groupby(['mmsi', 'time_order'])['geometry']
    .apply(create_linestring)
    .dropna()
)

# Create a GeoDataFrame for track lines
track_lines_gdf = gpd.GeoDataFrame(track_lines, geometry='geometry', crs=crs)

# Save to GeoPackage
output_file = "AIS_all_track_line_20220811.gpkg"
try:
    track_lines_gdf.to_file(output_file, layer='AIS_all_track_line_20220811', driver="GPKG")
    print(f"Track lines saved to {output_file}")
except Exception as e:
    raise RuntimeError(f"Failed to save GeoPackage: {e}")

# Plot results
try:
    plt.figure(figsize=(12, 8))
    track_lines_gdf.plot()
    plt.title("AIS Vessel Tracks")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.show()
except Exception as e:
    raise RuntimeError(f"Failed to plot data: {e}")
