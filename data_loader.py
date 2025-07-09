import geopandas as gpd
import rasterio
import json

def load_villages():
    return gpd.read_file('data/pune_villages.geojson')

def load_soil():
    return gpd.read_file('data/soil.geojson')

def load_rivers():
    return gpd.read_file('data/rivers.geojson')

def load_highways():
    return gpd.read_file('data/highways.geojson')

def load_lulc():
    return rasterio.open('data/resampled_lulc.tif')

def load_elevation():
    return rasterio.open('data/rescaled_Elevation.tif')

def load_usecases():
    with open('data/enhanced_usecases.txt', encoding='utf-8') as f:
        return f.read().splitlines()

def load_crop_knowledge():
    with open('data/crop_knowledge.json', encoding='utf-8') as f:
        return json.load(f)
