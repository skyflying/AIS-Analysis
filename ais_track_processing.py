
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
from pyproj import CRS

# Read Excel file
vessel = pd.read_excel("AIS_data_20220811.xlsx")

# Sort and handle missing values
vessel = vessel.sort_values(["mmsi"], ascending=True)
missing_values = vessel.isnull().sum()
print("Missing values statistics:\n", missing_values)
vessel = vessel.drop(labels=['vessel_type_main','vessel_type_sub'], axis='columns')

# Create geometry objects
geometry = [Point(xy) for xy in zip(vessel.longitude, vessel.latitude)]
crs = CRS("epsg:4326")

# Process time data and create GeoDataFrame
time_order = vessel['ts_pos_utc'].round(-6)
df = gpd.GeoDataFrame(vessel, crs=crs, geometry=geometry)
df = df.assign(time_order=time_order)

# Filter and group data
test = df.groupby(['mmsi']).filter(lambda x: len(x) > 5)
test = test.sort_values(['ts_pos_utc'], ascending=True)

# Generate track lines
def create_linestring(x):
    if len(x) > 1:
        return LineString(x.tolist())
    else:
        return None

df_final = test.groupby(['mmsi', 'time_order'])['geometry'].apply(create_linestring).dropna()
df_final = gpd.GeoDataFrame(df_final, geometry='geometry', crs=crs)

# Plot and save results
df_final.plot()
df_final.to_file("AIS_all_track_line_20220811.gpkg", layer='AIS_all_track_line_20220811', driver="GPKG")
