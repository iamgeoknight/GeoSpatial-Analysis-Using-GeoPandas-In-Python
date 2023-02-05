import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

#Read datasets
uk_accidents = pd.read_csv('data/uk_accidents/Accident_Information.tar.xz', low_memory=False)


# Convert Long Lat into numeric type
uk_accidents['Longitude'] = pd.to_numeric(uk_accidents['Longitude'])
uk_accidents['Latitude'] = pd.to_numeric(uk_accidents['Latitude'])


#  Convert Longitude Latitude into Point Geometry
uk_accidents = gpd.GeoDataFrame(uk_accidents, geometry = gpd.points_from_xy(x=uk_accidents['Longitude'], y=uk_accidents['Latitude']))
uk_accidents = uk_accidents.set_crs('EPSG:4326')

# Remove invalid geometries if any
uk_accidents = uk_accidents[uk_accidents.is_valid]
uk_accidents = uk_accidents[~uk_accidents.is_empty]
uk_accidents = uk_accidents.to_crs('EPSG:3857')


# Perform spatial queries, such as finding accidents within a certain distance from a specific location:

# Creating a sample point
point = Point((-13411.1, 6711284.0))

# Creating a buffer of 1 KM around the point
buffer = point.buffer(1000)

within_buffer = uk_accidents[uk_accidents.within(buffer)]


# Load the administrative regions shapefile
uk_admins = gpd.read_file('data/uk_admin_region/uk_admins_region.shp')
uk_admins = uk_admins.to_crs('EPSG:3857')

# Perform a spatial join between the accidents GeoDataFrame and the administrative regions shapefile
merged = gpd.sjoin(uk_accidents, uk_admins, how="inner", predicate='within')

# Group the merged GeoDataFrame by the administrative region and count the number of accidents in each region
grouped = merged.groupby('ADMIN_REGI').count()['Accident_Index']


