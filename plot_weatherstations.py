import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx

#https://data.gov.hk/en-data/dataset/hk-dpo-datagovhk2-city-dashboard-weather-station
# Create DataFrame
df =  pd.read_csv('resources/weather-station-info.csv')

# Create GeoDataFrame
geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Convert to Web Mercator for background map
gdf_web_mercator = gdf.to_crs(epsg=3857)

# Create plot
fig, ax = plt.subplots(figsize=(12, 8))
gdf_web_mercator.plot(ax=ax, color='red', markersize=100, alpha=0.8, edgecolor='black')

# Add background map
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Add labels
for x, y, label in zip(gdf_web_mercator.geometry.x, gdf_web_mercator.geometry.y, gdf_web_mercator['station_name_en']):
    ax.annotate(label, xy=(x, y), xytext=(5, 5), textcoords="offset points",
                fontsize=10, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))

plt.title('Geographic Points Map', fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.show()

